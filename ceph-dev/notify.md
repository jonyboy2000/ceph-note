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
  argv_to_vec(argc, (const char **)argv, args);
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
    std::list<TopicConfiguration> rules;
  public:
    NotificationConfiguration() {}
    int get_rules_length(){return rules.size();}
    std::list<TopicConfiguration>& get_rules(){return rules;}
    ~NotificationConfiguration() {}

  void encode(bufferlist& bl) const {
    ENCODE_START(1, 1, bl);
    encode(rules, bl);
    ENCODE_FINISH(bl);
  }
  void decode(bufferlist::const_iterator& bl) {
    DECODE_START(1, bl);
    decode(rules, bl);
    DECODE_FINISH(bl);
  }
  void dump(Formatter *f) const;
};
WRITE_CLASS_ENCODER(NotificationConfiguration)



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
  bool xml_end(const char *el) override;
//  void to_xml(ostream& out);
  std::string& get_prefix(){ return prefix;}
  std::string& get_suffix(){ return suffix;}
};

bool FilterRule_S3::xml_end(const char *el) {
  XMLObjIter iter = find("FilterRule");
  FilterRule_S3 *obj;
  if (!(obj = static_cast<FilterRule_S3 *>(iter.get_next()))) {
    std::cout << "FilterRule_S3 should have atleast one" << std::endl;
    return false;
  }
  for(; obj; obj = static_cast<FilterRule_S3 *>(iter.get_next())) {
    std::string _name, _val;
    RGWXMLDecoder::decode_xml("Name", _name, obj);
    RGWXMLDecoder::decode_xml("Value", _val, obj);
    if (_name.compare("prefix") == 0 || _name.compare("Prefix") == 0 ) {
      prefix = _val;
    } else if (_name.compare("suffix") == 0 || _name.compare("Suffix") == 0 ) {
      suffix = _val;
    }
  }
  return true;
}


class S3Key_S3 : public XMLObj {
  FilterRule_S3 filter_rule;
public:
  S3Key_S3() {}
  ~S3Key_S3() override {}
  bool xml_end(const char *el) override;
  FilterRule_S3& get_filter_rule() { return filter_rule;}
};

bool S3Key_S3::xml_end(const char *el) {
  XMLObjIter iter = find("FilterRule");
  FilterRule_S3 *obj;
  if (!(obj = static_cast<FilterRule_S3 *>(iter.get_next()))) {
    std::cout << "S3Key_S3 should have atleast one" << std::endl;
    return false;
  }
  filter_rule = *obj;
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
  XMLObjIter iter = find("S3Key");
  S3Key_S3 *obj;
  if (!(obj = static_cast<S3Key_S3 *>(iter.get_next()))) {
    std::cout << "Filter_S3 should have atleast one" << std::endl;
    return false;
  }
  s3key = *obj;
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
  public:
    TopicConfiguration_S3() {}
    ~TopicConfiguration_S3() override {}
    
    bool xml_end(const char *el) override;
    void to_xml(XMLFormatter& f);
};

class NotificationConfiguration_S3 : public NotificationConfiguration, public XMLObj
{
  public:
    NotificationConfiguration_S3() {}
    ~NotificationConfiguration_S3() override {}
    bool xml_end(const char *el) override;
    void to_xml(ostream& out);
};

class NotificationConfigurationXMLParser_S3 : public RGWXMLParser
{
  CephContext *cct;
  XMLObj *alloc_obj(const char *el) override;
public:
  explicit NotificationConfigurationXMLParser_S3(CephContext *_cct) : cct(_cct) {}
};


void TopicConfiguration_S3::to_xml(XMLFormatter& f) {
  f.open_object_section("TopicConfiguration");
  if (id.length() > 0) {
    f.dump_string("Id", id);
  }
  if (topic.length() > 0) {
    f.dump_string("Topic", topic);
  }
  for(list<string>::iterator it = events.begin(); it != events.end(); ++it) {
    f.dump_string("Event", *it);
  }
  f.close_section();
}
class Filter_S3;
bool TopicConfiguration_S3::xml_end(const char *el) {
  XMLObj *o = find_first("Id");
  id.clear();
  id = o->get_data();

  o = find_first("Topic");
  topic.clear();
  topic = o->get_data();

  XMLObjIter iter = find("Event");
  XMLObj *obj;
  obj = iter.get_next();
  if (obj) {
    for( ; obj; obj = iter.get_next()) {
      const char *s = obj->get_data().c_str();
      std::cout  << "TopicConfiguration_S3::xml_end, el : " << el << ", data : " << s << std::endl;
      if (s) {
        events.push_back(string(s));
      } else {
        return false;
      }
    }
  }

//  iter = find("Filter");
//  obj = iter.get_next();
//  if(obj) {
//    prefix = static_cast<Filter_S3 *>(obj)->get_s3key().get_filter_rule().get_prefix();
//    suffix = static_cast<Filter_S3 *>(obj)->get_s3key().get_filter_rule().get_suffix();
//  }
  return true;
}

void NotificationConfiguration_S3::to_xml(ostream& out) {
  XMLFormatter f;
  f.open_object_section_in_ns("NotificationConfiguration", XMLNS_AWS_S3);
  for(list<TopicConfiguration>::iterator it = rules.begin();
      it != rules.end(); ++it) {
    (static_cast<TopicConfiguration_S3 &>(*it)).to_xml(f);
  }
  f.close_section();
  f.flush(out);
}

bool NotificationConfiguration_S3::xml_end(const char *el) {
  XMLObjIter iter = find("TopicConfiguration");
  TopicConfiguration_S3 *obj;
  if (!(obj = static_cast<TopicConfiguration_S3 *>(iter.get_next()))) {
    std::cout << "NotificationConfiguration should have atleast one" << std::endl;
    return false;
  }
  for(; obj; obj = static_cast<TopicConfiguration_S3 *>(iter.get_next())) {
    rules.push_back(*obj);
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
    return new NotificationConfiguration_S3;
  } else if (strcmp(el, "TopicConfiguration") == 0) {
    return new TopicConfiguration_S3;
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
    NotificationConfiguration_S3 *bn_config;
//string data = string("<BNConfiguration></BNConfiguration>");
    string data = string("<NotificationConfiguration><TopicConfiguration><Id>1</Id><Topic>one</Topic><Event>GET</Event><Filter><S3Key><FilterRule><Name>Suffix</Name><Value>.jpg</Value></FilterRule></S3Key></Filter></TopicConfiguration><TopicConfiguration><Id>2</Id><Topic>two</Topic><Event>PUT</Event><Event>DELETE</Event><Filter><S3Key><FilterRule><Name>Suffix</Name><Value>.png</Value><Name>Prefix</Name><Value>dir1/</Value></FilterRule></S3Key></Filter></TopicConfiguration></NotificationConfiguration>");
    parser.init();
    parser.parse(data.c_str(), data.length(), 1);
    bn_config = static_cast<NotificationConfiguration_S3 *>(parser.find_first(
                         "NotificationConfiguration"));

    std::cout << "length(): " << bn_config->get_rules_length() << std::endl;

    std::list<TopicConfiguration> rules =bn_config->get_rules();
    for(list<TopicConfiguration>::iterator it = rules.begin();it != rules.end(); ++it) {
      std::cout << "TopicConfiguration>>" << std::endl;
      std::cout << (*it).get_id() << std::endl;
      std::cout << (*it).get_prefix() << std::endl;
      std::cout << (*it).get_suffix() << std::endl;
      std::cout << (*it).get_topic() << std::endl;
      for(list<std::string>::iterator eit = (*it).get_events().begin();eit != (*it).get_events().end(); ++eit) {
        std::cout << (*eit) << std::endl;
    }

//        auto topic = (static_cast<TopicConfiguration_S3 &>(*it));
//        std::cout << topic.get_id() << topic.get_topic();
////        auto event = topic.get_events();
////        for(list<std::string>::iterator eit = event.begin();eit != event.end(); ++eit) {
////            std::cout << *eit << std::endl;
////        }
    }


    stringstream ss;
    bn_config->to_xml(ss);
    std::cout << ss.str() << std::endl;

//cat c = cat();
//std::cout << c.miao() << std::endl;

// RGWBucketAdminOpState bucket_op;
// bucket_op.set_bucket_name("test1");
// int ret = RGWBucketAdminOp::dump_s3_policy(store, bucket_op, std::cout);
// std::cout << std::endl;
}


```
