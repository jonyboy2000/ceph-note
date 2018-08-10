```
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <time.h>
#include <sys/wait.h>
#include <unistd.h>
#include <fstream>
#include <map>
#include <list>
extern "C"{
#include <curl/curl.h>
}
#include "common/ceph_crypto.h"
#include "include/str_list.h"
#include "common/ceph_json.h"
#include "common/code_environment.h"
#include "common/ceph_argparse.h"
#include "common/Finisher.h"
#include "global/global_init.h"
#include "rgw/rgw_common.h"
#include "rgw/rgw_bucket.h"
#include "rgw/rgw_rados.h"
#include "include/utime.h"
#include "include/object.h"
#include "cls/statelog/cls_statelog_types.h"
#include <gtest/gtest.h>
#define XMLNS_AWS_S3 "http://s3.amazonaws.com/doc/2006-03-01/"
#include "cat.h"
using namespace std;

RGWRados *store;

int main(int argc, char *argv[]){
  vector<const char*> args;
  args.push_back("--conf=/ceph/ceph/build/cluster1/ceph.conf");
//  argv_to_vec(argc, (const char **)argv, args);
  auto cct = global_init(NULL, args, CEPH_ENTITY_TYPE_CLIENT,
             CODE_ENVIRONMENT_UTILITY,
             CINIT_FLAG_NO_DEFAULT_CONFIG_FILE);
  common_init_finish(g_ceph_context);
  store = RGWStoreManager::get_storage(g_ceph_context, false, false, false, false, false);
  ::testing::InitGoogleTest(&argc, argv);
  int r = RUN_ALL_TESTS();
  return 0;
}

class TopicConfiguration
{
protected:
  std::string id;
  std::string topic;
  std::list<string> events;
  std::string prefix;
  std::string suffix;
public:
  TopicConfiguration() {}
  virtual ~TopicConfiguration() {}
  std::string& get_id() { return id; }
  std::string& get_prefix() { return prefix; }
  std::string& get_suffix() { return suffix; }
  std::string& get_topic() { return topic; }
  std::list<string>& get_events() { return events; }
  void set_id(std::string _i) { id = _i; }
  void set_prefix(std::string _p) { prefix = _p; }
  void set_suffix(std::string _s) { suffix = _s; }
  void set_events(std::list<string> _e) { events = _e; }
  void encode(bufferlist& bl) const {
    ENCODE_START(1, 1, bl);
    encode(id, bl);
    encode(topic, bl);
    encode(events, bl);
    encode(prefix, bl);
    encode(suffix, bl);
    ENCODE_FINISH(bl);
  }
  void decode(bufferlist::const_iterator& bl) {
    DECODE_START(1, bl);
    decode(id, bl);
    decode(topic, bl);
    decode(events, bl);
    decode(prefix, bl);
    decode(suffix, bl);
    DECODE_FINISH(bl);
  }
};
WRITE_CLASS_ENCODER(TopicConfiguration)

class NotificationConfiguration
{
protected:
  std::map<string, TopicConfiguration> tcs_map;
  std::list<TopicConfiguration> tcs;
public:
  NotificationConfiguration() {}
  int get_tcs_length(){return tcs.size();}
  std::list<TopicConfiguration>& get_tcs(){return tcs;}
  std::map<string, TopicConfiguration>& get_tcs_map(){return tcs_map;}
  int check_and_add_topic_config(TopicConfiguration *tc);
  ~NotificationConfiguration() {}

  void encode(bufferlist& bl) const {
    ENCODE_START(1, 1, bl);
    encode(tcs, bl);
    ENCODE_FINISH(bl);
  }
  void decode(bufferlist::const_iterator& bl) {
    DECODE_START(1, bl);
    decode(tcs, bl);
    DECODE_FINISH(bl);
  }
  void dump(Formatter *f) const;
};
WRITE_CLASS_ENCODER(NotificationConfiguration)

static inline int validate_event(const std::string& o) {
  std::cout << o << std::endl;
  if (o.compare("s3:ObjectCreated:*") == 0 || o.compare("s3:ObjectCreated:Put") == 0 || o.compare("s3:ObjectCreated:Post") == 0 \
      || o.compare("s3:ObjectCreated:Copy") == 0 || o.compare("s3:ObjectCreated:CompleteMultipartUpload") == 0 \
      || o.compare("s3:ObjectRemoved:*") == 0 || o.compare("s3:ObjectRemoved:Delete") == 0 \
      || o.compare("s3:ObjectRemoved:DeleteMarkerCreated") == 0 || o.compare("s3:ReducedRedundancyLostObject") == 0 \
   )
    return 0;
  return -1;
}

static inline bool samerule(std::string r1, std::string r2) {
  if (r1.length() != r2.length())
    return false;
  int count = 0;
  for(int i=0; i< r1.length(); i++) {
    if (r1.at(i) == r2.at(i) || r1.at(i) == '*' || r2.at(i) == '*') {
      count++;
      continue;
    }
  }
  if (count == r1.length()){
    std::cout << "samerule: true" << std::endl;
    return true;
  }
  std::cout << "samerule: false" << std::endl;

  return false;
}

static inline bool sameevent(std::list<std::string> e1, std::list<std::string> e2) {
  std::cout << "sameevent: start" << std::endl;
  for (std::list<std::string>::iterator i = e1.begin(); i != e1.end() ; i++) {
    for (std::list<std::string>::iterator j = e2.begin(); j != e2.end() ; j++) {
      std::string event1 = *i;
      std::string event2 = *j;
      if (event1.compare(event2) == 0 \
 || (event1.compare("s3:ObjectCreated:*") == 0 && (event2.find("s3:ObjectCreated") != std::string::npos)) \
 || (event2.compare("s3:ObjectCreated:*") == 0 && (event1.find("s3:ObjectCreated") != std::string::npos)) \
 || (event1.compare("s3:ObjectRemoved:*") == 0 && (event2.find("s3:ObjectRemoved") != std::string::npos)) \
 || (event2.compare("s3:ObjectRemoved:*") == 0 && (event1.find("s3:ObjectRemoved") != std::string::npos))) {
//        std::cout << "sameevent: same event found" << std::endl;
//        std::cout << "event1: " << event1 << " event2:" << event2 << std::endl;
        return true;
      }
    }
  }
  return false;
}

#define s3_ObjectCreated_Put 0x1
#define s3_ObjectCreated_Post 0x2
#define s3_ObjectCreated_Copy 0x4
#define s3_ObjectCreated_CompleteMultipartUpload 0x8
#define s3_ObjectCreated_ALL (s3_ObjectCreated_Put    |  \
                         s3_ObjectCreated_Post    |  \
                         s3_ObjectCreated_Copy   |  \
                         s3_ObjectCreated_CompleteMultipartUpload)


#define s3_ObjectRemoved_Delete 0x10
#define s3_ObjectRemoved_DeleteMarkerCreated 0x20
#define s3_ObjectRemoved_ALL (s3_ObjectRemoved_Delete    |  \
                         s3_ObjectRemoved_DeleteMarkerCreated)

#define s3_ReducedRedundancyLostObject 0x100

int NotificationConfiguration::check_and_add_topic_config(TopicConfiguration *tc) {
  string id, topic;

  //check Id
  id = tc->get_id();
  if (tcs_map.find(id) != tcs_map.end()) {   //Id shouldn't be the same
    return -EINVAL;
  }
  //check Topic
  topic = tc->get_topic();
  if (topic.empty()) {   //Topic not empty
    return -EINVAL;
  }
  // check Event
  std::set<std::string> events;
  int ObjectCreatedEventSum = 0;
  int ObjectRemovedEventSum = 0;
  int ReducedRedundancyLostObjectSum = 0;
  for(std::list<std::string>::iterator eit = tc->get_events().begin();
      eit != tc->get_events().end();
      ++eit) {
    const std::string event = *eit;

    if (validate_event(event) !=0 )
      return -EINVAL;

    if (events.find(event) != events.end()){
      std::cout << "find same event" << std::endl;
      return -EINVAL;
    } else {
      events.insert(events.end(), event);
    }

    if (event.compare("s3:ObjectCreated:Put") == 0) {
      ObjectCreatedEventSum += s3_ObjectCreated_Put;
    } else if (event.compare("s3:ObjectCreated:Post") == 0) {
      ObjectCreatedEventSum += s3_ObjectCreated_Post;
    } else if (event.compare("s3:ObjectCreated:Copy") == 0) {
      ObjectCreatedEventSum += s3_ObjectCreated_Copy;
    } else if (event.compare("s3:ObjectCreated:CompleteMultipartUpload") == 0) {
      ObjectCreatedEventSum += s3_ObjectCreated_CompleteMultipartUpload;
    } else if (event.compare("s3:ObjectCreated:*") == 0) {
      ObjectCreatedEventSum += s3_ObjectCreated_ALL;
    } else if (event.compare("s3:ObjectRemoved:Delete") == 0) {
      ObjectRemovedEventSum += s3_ObjectRemoved_Delete;
    } else if (event.compare("s3:ObjectRemoved:DeleteMarkerCreated") == 0) {
      ObjectRemovedEventSum += s3_ObjectRemoved_DeleteMarkerCreated;
    } else if (event.compare("s3:ObjectRemoved:*") == 0) {
      ObjectRemovedEventSum += s3_ObjectRemoved_ALL;
    } else {
      ReducedRedundancyLostObjectSum += s3_ReducedRedundancyLostObject;
    }
  }
  if (events.size() == 0)
    return -EINVAL;

  std::cout << "ObjectCreatedEventSum: " << ObjectCreatedEventSum << std::endl;
  std::cout << "ObjectRemovedEventSum: " << ObjectRemovedEventSum << std::endl;
  std::cout << "ReducedRedundancyLostObjectSum: " << ReducedRedundancyLostObjectSum << std::endl;
  if (ObjectCreatedEventSum > s3_ObjectCreated_ALL)
    return -EINVAL;
  if (ObjectRemovedEventSum > s3_ObjectRemoved_ALL)
    return -EINVAL;
  if (ReducedRedundancyLostObjectSum > s3_ReducedRedundancyLostObject)
    return -EINVAL;

  tcs_map.insert(std::pair<string, TopicConfiguration>(id, *tc));
}

class Id_S3 : public XMLObj {
public:
  Id_S3() {}
  ~Id_S3() override {}
};
class Topic_S3 : public XMLObj {
public:
  Topic_S3() {}
  ~Topic_S3() override {}
};
class Event_S3 : public XMLObj {
public:
  Event_S3() {}
  ~Event_S3() override {}
};


class FilterRule_S3 : public XMLObj {
  std::string prefix;
  std::string suffix;
public:
  FilterRule_S3() {}
  ~FilterRule_S3() override {}
  std::string& get_prefix(){ return prefix;}
  std::string& get_suffix(){ return suffix;}
  void set_prefix(std::string _prefix){ prefix = _prefix;}
  void set_suffix(std::string _suffix){ suffix = _suffix;}
};

class S3Key_S3 : public XMLObj {
  FilterRule_S3 prefix_filter_rule;
  FilterRule_S3 suffix_filter_rule;
public:
  S3Key_S3() {}
  ~S3Key_S3() override {}
  bool xml_end(const char *el) override;
  FilterRule_S3& get_prefix_filter_rule() { return prefix_filter_rule;}
  FilterRule_S3& get_suffix_filter_rule() { return suffix_filter_rule;}
};

bool S3Key_S3::xml_end(const char *el) {
  XMLObjIter iter = find("FilterRule");
  FilterRule_S3 *obj;
  if (!(obj = static_cast<FilterRule_S3 *>(iter.get_next()))) {
    return false;
  }
  for(; obj; obj = static_cast<FilterRule_S3 *>(iter.get_next())) {
    std::string _name, _val;
    RGWXMLDecoder::decode_xml("Name", _name, obj);
    RGWXMLDecoder::decode_xml("Value", _val, obj);
    if (_name.compare("prefix") == 0 || _name.compare("Prefix") == 0 ) {
      prefix_filter_rule = *obj;
      prefix_filter_rule.set_prefix(_val);
    } else if (_name.compare("suffix") == 0 || _name.compare("Suffix") == 0 ) {
      suffix_filter_rule = *obj;
      suffix_filter_rule.set_suffix(_val);
    } else {
      return false;
    }
  }
  return true;
}

class Filter_S3 : public XMLObj {
  S3Key_S3 s3key;
public:
  Filter_S3() {}
  ~Filter_S3() override {}
  bool xml_end(const char *el) override;
  S3Key_S3& get_s3key() { return s3key;}
};

bool Filter_S3::xml_end(const char *el) {
  S3Key_S3 *s3key_obj = static_cast<S3Key_S3 *>(find_first("S3Key"));
  s3key = *s3key_obj;
  return true;
}

class Name_S3 : public XMLObj {
public:
  Name_S3() {}
  ~Name_S3() override {}
};

class Value_S3 : public XMLObj {
public:
  Value_S3() {}
  ~Value_S3() override {}
};

class TopicConfiguration_S3 : public TopicConfiguration, public XMLObj
{
private:
  CephContext *cct;
public:
  TopicConfiguration_S3(): cct(nullptr) {}
  explicit TopicConfiguration_S3(CephContext *_cct): cct(_cct) {}
  ~TopicConfiguration_S3() override {}
    
  bool xml_end(const char *el) override;
  void to_xml(ostream& out);
  void dump_xml(Formatter* f) const;
  void set_ctx(CephContext *ctx) {
    cct = ctx;
  }
};

void TopicConfiguration_S3::dump_xml(Formatter* f) const {
  f->open_object_section("TopicConfiguration");
  encode_xml("Id", id, f);
  encode_xml("Topic", topic, f);
  for(std::list<std::string>::const_iterator it = events.begin();
      it != events.end();
      ++it) {
    encode_xml("Event", *it, f);
  }
  if (!prefix.empty() || !suffix.empty()) {
    f->open_object_section("Filter");
    f->open_object_section("S3Key");
    if (!prefix.empty()) {
      f->open_object_section("FilterRule");
      encode_xml("Name", "Preifx", f);
      encode_xml("Value", prefix, f);
      f->close_section();
    }
    if (!suffix.empty()) {
      f->open_object_section("FilterRule");
      encode_xml("Name", "Suffix", f);
      encode_xml("Value", suffix, f);
      f->close_section();
    }
    f->close_section();
    f->close_section();
  }
  f->close_section(); // topicconfigration
}

class NotificationConfiguration_S3 : public NotificationConfiguration, public XMLObj
{
private:
  CephContext *cct;
public:
  NotificationConfiguration_S3(): cct(nullptr) {}
  explicit NotificationConfiguration_S3(CephContext *_cct) : cct(_cct) {}
  ~NotificationConfiguration_S3() override {}
  bool xml_end(const char *el) override;
  void to_xml(ostream& out);
  void dump_xml(Formatter* f) const;
  int rebuild(RGWRados *store, NotificationConfiguration& dest);
  void set_ctx(CephContext *ctx) {
    cct = ctx;
  }
};

void NotificationConfiguration_S3::dump_xml(Formatter* f) const {
  f->open_object_section_in_ns("NotificationConfiguration", XMLNS_AWS_S3);

  for (auto iter = tcs_map.begin(); iter != tcs_map.end(); ++iter) {
    const TopicConfiguration_S3& topic_config = static_cast<const TopicConfiguration_S3&>(iter->second);
    topic_config.dump_xml(f);
  }

  f->close_section(); // notification
}

#define TOPICCONFIGURATION_ID_MAX_LEN     48
#define TOPICCONFIGURATION_PREFIX_MAX_LEN 48
#define TOPICCONFIGURATION_SUFFIX_MAX_LEN 48
#define TOPICCONFIGURATION_MAX_NUM        5

int NotificationConfiguration_S3::rebuild(RGWRados *store, NotificationConfiguration& dest) {
  if (tcs.size() > TOPICCONFIGURATION_MAX_NUM)
    return -EINVAL;

  int ret = 0;
  int rule_len_max = 0;
  for(list<TopicConfiguration>::iterator it = tcs.begin();
      it != tcs.end(); ++it) {
    TopicConfiguration& src_tc = *it;
    if (src_tc.get_id().length() > TOPICCONFIGURATION_ID_MAX_LEN)
      return -EINVAL;
    if (src_tc.get_prefix().length() > TOPICCONFIGURATION_PREFIX_MAX_LEN)
      return -EINVAL;
    if (src_tc.get_suffix().length() > TOPICCONFIGURATION_SUFFIX_MAX_LEN)
      return -EINVAL;
    //check rules
    int rule_length = src_tc.get_prefix().length() + src_tc.get_suffix().length();
    if (rule_length > rule_len_max)
      rule_len_max = rule_length;

    ret = dest.check_and_add_topic_config(&src_tc);
    if (ret < 0)
      return ret;
  }
  std::vector<std::string> rules;
  std::vector<std::list<std::string>> events;

  for(list<TopicConfiguration>::iterator it = tcs.begin();
      it != tcs.end(); ++it) {
    TopicConfiguration& src_tc = *it;
    if(src_tc.get_prefix().length() + src_tc.get_suffix().length() <= rule_len_max) {
      std::string tmpr = src_tc.get_prefix() + std::string((rule_len_max - src_tc.get_prefix().length() - \
      src_tc.get_suffix().length()), '*') +src_tc.get_suffix();
      std::cout << tmpr << std::endl;
      rules.push_back(tmpr);
      events.push_back(src_tc.get_events());
    }
  }

  for (int i = 0; i < rules.size(); i++) {
    for (int j = i+1; j < rules.size(); j++) {
      std::cout << "compare rule: " << rules.at(i) << "<-->" << rules.at(j) << std::endl;
      if (samerule(rules.at(i) , rules.at(j))){
        if (sameevent(events.at(i), events.at(j))) {
          std::cout << "found same rule" << std::endl;
          std::cout << rules.at(i) << "<->" <<  rules.at(j) <<std::endl;
          return -EINVAL;
        }
      }
    }
  }

  return ret;
}

class NotificationConfigurationXMLParser_S3 : public RGWXMLParser
{
  CephContext *cct;
  XMLObj *alloc_obj(const char *el) override;
public:
  explicit NotificationConfigurationXMLParser_S3(CephContext *_cct) : cct(_cct) {}
};


void TopicConfiguration_S3::to_xml(ostream& out) {
  out << "<TopicConfiguration>";
  if (!id.empty())
    out << "<Id>" << id << "</Id>";
  if (!topic.empty())
    out << "<Topic>" << topic << "</Topic>";
  for(std::list<string>::iterator it = events.begin();
      it != events.end();
      ++it) {
    out << "<Event>" << *it << "</Event>";
  }
  if (!prefix.empty() || !suffix.empty()) {
    out << "<Filter>";
    out << "<S3Key>";
    if (!prefix.empty()) {
      out << "<FilterRule>";
      out << "<Name>Prefix</Name>";
      out << "<Value>" <<  prefix << "</Value>";
      out << "</FilterRule>";
    }
    if (!suffix.empty()) {
      out << "<FilterRule>";
      out << "<Name>Suffix</Name>";
      out << "<Value>" <<  suffix << "</Value>";
      out << "</FilterRule>";
    }
    out << "</S3Key>";
    out << "</Filter>";
  }
  out << "</TopicConfiguration>";
}

bool TopicConfiguration_S3::xml_end(const char *el) {
  XMLObj *o = find_first("Id");
  if (o) {
    id.clear();
    id = o->get_data();
  } else {
    char buf[TOPICCONFIGURATION_ID_MAX_LEN + 1];
    gen_rand_alphanumeric_lower(cct, buf, sizeof(buf));
    id = std::string(buf);
  }

  o = find_first("Topic");
  if (!o) {
    std::cout  << "Topic not found" << std::endl;
  } else {
    topic.clear();
    topic = o->get_data();
  }

  XMLObjIter iter = find("Event");
  XMLObj *obj;
  obj = iter.get_next();
  if (obj) {
    for( ; obj; obj = iter.get_next()) {
      std::string s = obj->get_data();
      std::cout  << "TopicConfiguration_S3::xml_end, el : " << el << ", data : " << s << std::endl;
      if (!s.empty()) {
        events.push_back(string(s));
      }
    }
  }
  iter = find("Filter");
  obj = iter.get_next();
  if(obj) {
    prefix = static_cast<Filter_S3 *>(obj)->get_s3key().get_prefix_filter_rule().get_prefix();
    suffix = static_cast<Filter_S3 *>(obj)->get_s3key().get_suffix_filter_rule().get_suffix();
  }
  return true;
}

void NotificationConfiguration_S3::to_xml(ostream& out) {
  out << "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" ;
  out << "<NotificationConfiguration xmlns=\"http://s3.amazonaws.com/doc/2006-03-01/>";
  for(list<TopicConfiguration>::iterator it = tcs.begin();
      it != tcs.end(); ++it) {
    (static_cast<TopicConfiguration_S3 &>(*it)).to_xml(out);
  }
  out << "</NotificationConfiguration>";
}

bool NotificationConfiguration_S3::xml_end(const char *el) {
  XMLObjIter iter = find("TopicConfiguration");
  TopicConfiguration_S3 *obj;
  if (!(obj = static_cast<TopicConfiguration_S3 *>(iter.get_next()))) {
    return false;
  }
  for(; obj; obj = static_cast<TopicConfiguration_S3 *>(iter.get_next())) {
    tcs.push_back(*obj);
  }
  return true;
}

class RGWNotificationConfigurationXMLParser_S3 : public RGWXMLParser
{
  CephContext *cct;

  XMLObj *alloc_obj(const char *el) override;
public:
  explicit RGWNotificationConfigurationXMLParser_S3(CephContext *_cct) : cct(_cct) {}
};

XMLObj *RGWNotificationConfigurationXMLParser_S3::alloc_obj(const char *el) {
  if (strcmp(el, "NotificationConfiguration") == 0) {
    return new NotificationConfiguration_S3(cct);
  } else if (strcmp(el, "TopicConfiguration") == 0) {
    return new TopicConfiguration_S3(cct);
  } else if (strcmp(el, "Id") == 0) {
    return new Id_S3;
  } else if (strcmp(el, "Topic") == 0) {
    return new Topic_S3;
  } else if (strcmp(el, "Event") == 0) {
    return new Event_S3;
  } else if (strcmp(el, "Filter") == 0) {
    return new Filter_S3;
  } else if (strcmp(el, "S3Key") == 0) {
    return new S3Key_S3;
  } else if (strcmp(el, "FilterRule") == 0) {
    return new FilterRule_S3;
  } else if (strcmp(el, "Name") == 0) {
    return new Name_S3;
  } else if (strcmp(el, "Value") == 0) {
    return new Value_S3;
  }
  return NULL;
}

TEST  (test1, run1) {

    RGWNotificationConfigurationXMLParser_S3 parser(store->ctx());
    NotificationConfiguration_S3 *bn_config_s3;
//    bn_config_s3->set_ctx(store->ctx());
//    string data = string("<NotificationConfiguration><TopicConfiguration><Id>1</Id><Topic>one</Topic><Event>s3:ObjectCreated:Put</Event><Filter><S3Key><FilterRule><Name>Suffix</Name><Value>.jpg</Value></FilterRule><FilterRule><Name>Prefix</Name><Value>1/</Value></FilterRule></S3Key></Filter></TopicConfiguration><TopicConfiguration><Id>333</Id><Topic>three</Topic><Event>s3:ObjectCreated:Copy</Event><Event>s3:ObjectCreated:Post</Event><Filter><S3Key><FilterRule><Name>Suffix</Name><Value>.png</Value></FilterRule><FilterRule><Name>Prefix</Name><Value>image/</Value></FilterRule></S3Key></Filter></TopicConfiguration><TopicConfiguration><Id>2</Id><Topic>two</Topic><Event>s3:ObjectCreated:Copy</Event><Event>s3:ObjectCreated:Post</Event><Filter><S3Key><FilterRule><Name>Suffix</Name><Value>.png</Value></FilterRule><FilterRule><Name>Prefix</Name><Value>dir123/</Value></FilterRule></S3Key></Filter></TopicConfiguration></NotificationConfiguration>");
//    string data = string("<NotificationConfiguration><TopicConfiguration><Topic>one</Topic><Event>s3:ObjectCreated:Put</Event><Filter><S3Key><FilterRule><Name>Suffix</Name><Value>.jpg</Value></FilterRule></S3Key></Filter></TopicConfiguration></NotificationConfiguration>");
    string data = string("<NotificationConfiguration><TopicConfiguration><Id>1</Id><Topic>one</Topic><Event>s3:ObjectCreated:*</Event><Filter><S3Key><FilterRule><Name>Suffix</Name><Value>.jpg</Value></FilterRule><FilterRule><Name>Prefix</Name><Value>1</Value></FilterRule></S3Key></Filter></TopicConfiguration><TopicConfiguration><Id>333</Id><Topic>three</Topic><Event>s3:ObjectCreated:Put</Event><Filter><S3Key><FilterRule><Name>Suffix</Name><Value>.jpg</Value></FilterRule><FilterRule><Name>Prefix</Name><Value>11</Value></FilterRule></S3Key></Filter></TopicConfiguration></NotificationConfiguration>");
    parser.init();
    parser.parse(data.c_str(), data.length(), 1);
//    std::cout << "get_unallocated_objs_size: " << parser.get_unallocated_objs_size() << std::endl;

    bn_config_s3 = static_cast<NotificationConfiguration_S3 *>(parser.find_first("NotificationConfiguration"));
    std::cout << "length(): " << bn_config_s3->get_tcs_length() << std::endl;
    std::list<TopicConfiguration> tcs =bn_config_s3->get_tcs();
    for(list<TopicConfiguration>::iterator it = tcs.begin();it != tcs.end(); ++it) {
      std::cout << "TopicConfiguration>>" << std::endl;
      std::cout << "id: "<< (*it).get_id() << std::endl;
      std::cout << "prefix: "<<(*it).get_prefix() << std::endl;
      std::cout << "suffix: "<<(*it).get_suffix() << std::endl;
      std::cout << "topic: "<<(*it).get_topic() << std::endl;
      for(std::list<std::string>::iterator eit = (*it).get_events().begin();
        eit != (*it).get_events().end();
        ++eit) {
        std::cout << (*eit) << std::endl;
      }
    }
//  stringstream ss;
//  bn_config_s3->to_xml(ss);
//  std::cout << ss.str() << std::endl;

  NotificationConfiguration bn_config;
  int ret = bn_config_s3->rebuild(store, bn_config);
  std::cout << "ret: " << ret << std::endl;

//  if (ret == 0) {
//    std::map<string, TopicConfiguration> m = bn_config.get_tcs_map();
//    std::cout << "size(): " << m.size() << std::endl;
//    std::map<string, TopicConfiguration>::iterator iter;
//    for (iter = m.begin(); iter != m.end(); ++iter) {
//      TopicConfiguration obj = iter->second;
//      std::cout << obj.get_id() << std::endl;
//      std::cout << obj.get_prefix() << std::endl;
//      std::cout << obj.get_suffix() << std::endl;
//      for(std::list<std::string>::iterator eit = obj.get_events().begin(); eit != obj.get_events().end(); ++eit) {
//        std::cout << (*eit) << std::endl;
//      }
//    }
//  }
}


TEST  (test1, run2) {
  map<string, bufferlist> bucket_attrs;
  RGWBucketInfo bucket_info;
  RGWObjectCtx obj_ctx(store);
  int ret = store->get_bucket_info(obj_ctx, "", "test1", bucket_info, NULL, &bucket_attrs);
  if (ret < 0) {
    std::cout << "get_bucket_info for " << "test1" << " failed" << std::endl;
    return;
  }
  map<string, bufferlist>::iterator aiter = bucket_attrs.find(RGW_ATTR_BN);
  if (aiter == bucket_attrs.end()){
    std::cout << "RGW_ATTR_BN failed" << std::endl;
    return;
  }
  bufferlist::const_iterator iter{&aiter->second};
  NotificationConfiguration_S3 status;
  status.set_ctx(store->ctx());
  try {
    status.decode(iter);
  } catch (const buffer::error& e) {
    std::cout << "decode life cycle config failed" << std::endl;
    return;
  }
  std::map<string, TopicConfiguration> m = status.get_tcs_map();
//  std::cout << "size(): " << m.size() << std::endl;
//  std::map<string, TopicConfiguration>::iterator miter;
//  for (miter = m.begin(); miter != m.end(); ++miter) {
//    TopicConfiguration obj = miter->second;
//    std::cout << obj.get_id() << std::endl;
//    std::cout << obj.get_prefix() << std::endl;
//    std::cout << obj.get_suffix() << std::endl;
//    for(std::list<std::string>::iterator eit = obj.get_events().begin(); eit != obj.get_events().end(); ++eit) {
//      std::cout << (*eit) << std::endl;
//    }
//  }
  Formatter *f = new XMLFormatter(true);
  status.dump_xml(f);
  f->flush(std::cout);
}


//TEST  (test1, run2) {
//  RGWNotificationConfigurationXMLParser_S3 parser(store->ctx());
//  NotificationConfiguration_S3 *bn_config_s3;
//  string data = string("<NotificationConfiguration><TopicConfiguration><Topic>one</Topic><Event>s3:ObjectCreated:Put</Event><Filter><S3Key><FilterRule><Name>Suffix</Name><Value>.jpg</Value></FilterRule></S3Key></Filter></TopicConfiguration><TopicConfiguration><Id>2</Id><Topic>two</Topic><Event>s3:ObjectCreated:Copy</Event><Event>s3:ObjectCreated:Post</Event><Filter><S3Key><FilterRule><Name>Suffix</Name><Value>.png</Value></FilterRule><FilterRule><Name>Prefix</Name><Value>dir1/</Value></FilterRule></S3Key></Filter></TopicConfiguration></NotificationConfiguration>");
//  parser.init();
//  parser.parse(data.c_str(), data.length(), 1);
//  bn_config_s3 = static_cast<NotificationConfiguration_S3 *>(parser.find_first("NotificationConfiguration"));
//  std::cout << "length(): " << bn_config_s3->get_tcs_length() << std::endl;
//  std::list<TopicConfiguration> tcs =bn_config_s3->get_tcs();
//  for(list<TopicConfiguration>::iterator it = tcs.begin();it != tcs.end(); ++it) {
//    std::cout << "TopicConfiguration>>" << std::endl;
//    std::cout << (*it).get_id() << std::endl;
//    std::cout << (*it).get_prefix() << std::endl;
//    std::cout << (*it).get_suffix() << std::endl;
//    std::cout << (*it).get_topic() << std::endl;
//    for(std::set<std::string>::iterator eit = (*it).get_events().begin(); eit != (*it).get_events().end(); ++eit) {
//      std::cout << (*eit) << std::endl;
//    }
//  }
//  stringstream ss;
//  bn_config_s3->to_xml(ss);
//  std::cout << ss.str() << std::endl;

//  NotificationConfiguration bn_config;
//  int ret = bn_config_s3->rebuild(store, bn_config);
//  std::cout << "ret: " << ret << std::endl;
//  std::map<string, TopicConfiguration> m = bn_config.get_tcs_map();
//  std::cout << "size(): " << m.size() << std::endl;
//  std::map<string, TopicConfiguration>::iterator iter;
//
//  for (iter = m.begin(); iter != m.end(); ++iter) {
//    TopicConfiguration obj = iter->second;
//    std::cout << obj.get_id() << std::endl;
//    std::cout << obj.get_prefix() << std::endl;
//    std::cout << obj.get_suffix() << std::endl;
//    for(std::set<std::string>::iterator eit = obj.get_events().begin(); eit != obj.get_events().end(); ++eit) {
//      std::cout << (*eit) << std::endl;
//    }
//  }
//}
```
```
ceph-request put "/test1?notification" -c yly.request   --file noti.xml  --verbose

./bin/rados -p  default.rgw.meta  --namespace=root listxattr .bucket.meta.test1:0076671d-928c-4daa-8c3c-c304dfc2d891.14103.1  -c cluster1/ceph.conf
ceph.objclass.version
user.rgw.acl
user.rgw.bn
./bin/rados -p  default.rgw.meta  --namespace=root getxattr .bucket.meta.test1:0076671d-928c-4daa-8c3c-c304dfc2d891.14103.1  user.rgw.bn  -c cluster1/ceph.conf
image1^image1(arn:aws:sns:us-east-1:471863637113:images3:ObjectCreated:*1/.jpgimage2^image2(arn:aws:sns:us-east-1:471863637113:images3:ObjectCreated:*2/.jpg
```

noti.xml
```
<?xml version="1.0" encoding="UTF-8"?>
<NotificationConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <TopicConfiguration>
    <Id>image1</Id>
    <Topic>arn:aws:sns:us-east-1:471863637113:image</Topic>
    <Event>s3:ObjectCreated:*</Event>
    <Filter>
      <S3Key>
        <FilterRule>
          <Name>prefix</Name>
          <Value>1/</Value>
        </FilterRule>
        <FilterRule>
          <Name>Suffix</Name>
          <Value>.jpg</Value>
        </FilterRule>
      </S3Key>
    </Filter>
  </TopicConfiguration>
  <TopicConfiguration>
    <Id>image2</Id>
    <Topic>arn:aws:sns:us-east-1:471863637113:image</Topic>
    <Event>s3:ObjectCreated:*</Event>
    <Filter>
      <S3Key>
        <FilterRule>
          <Name>prefix</Name>
          <Value>2/</Value>
        </FilterRule>
        <FilterRule>
          <Name>Suffix</Name>
          <Value>.jpg</Value>
        </FilterRule>
      </S3Key>
    </Filter>
  </TopicConfiguration>
</NotificationConfiguration>
```

```
TEST  (test1, decode) {
  map<string, bufferlist> bucket_attrs;
  RGWBucketInfo bucket_info;
  RGWObjectCtx obj_ctx(store);
  std::string bucketname = std::string("test1");
  int ret = store->get_bucket_info(obj_ctx, "", bucketname.c_str(), bucket_info, NULL, &bucket_attrs);
  if (ret < 0) {
    std::cout << "get_bucket_info for " << bucketname.c_str() << " failed" << std::endl;
    return;
  }
  map<string, bufferlist>::iterator aiter = bucket_attrs.find(RGW_ATTR_BN);
  if (aiter == bucket_attrs.end()){
    std::cout << "get bucket xattr RGW_ATTR_BN failed" << std::endl;
    return;
  }
  bufferlist::const_iterator iter{&aiter->second};
  NotificationConfiguration_S3 status;
  status.set_ctx(store->ctx());
  try {
    status.decode(iter);
  } catch (const buffer::error& e) {
    std::cout << "decode bucket notification config failed" << std::endl;
    return;
  }
  std::map<string, TopicConfiguration> m = status.get_tcs_map();
  std::cout << "notification size(): " << m.size() << std::endl;
  std::map<string, TopicConfiguration>::iterator miter;
  for (miter = m.begin(); miter != m.end(); ++miter) {
    TopicConfiguration obj = miter->second;
    std::cout << obj.get_id() << std::endl;
    std::cout << obj.get_prefix() << std::endl;
    std::cout << obj.get_suffix() << std::endl;
    for(std::list<std::string>::iterator eit = obj.get_events().begin(); eit != obj.get_events().end(); ++eit) {
      std::cout << (*eit) << std::endl;
    }
  }
}
```


