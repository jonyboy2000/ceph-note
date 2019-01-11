import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.*;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

public class Main {
    static String accessKey = "yly";
    static String secretKey = "yly";
    static String cmd = "";
    static String resource = "";
    static String endPoint = "10.254.3.76:8084";

    public static void main(String[] args) throws Exception {
        cmd = "/refererbucket/?referer";
        resource = "/refererbucket/";
        String json_response = get();
        System.out.println(json_response);
    }
    //http get request
    public static String get() {
        HttpURLConnection conn = null;
        try {
            URL url = new URL("http://" + endPoint + cmd);
            conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            Date date = new Date();
            SimpleDateFormat dataformater = new SimpleDateFormat("EEE, d MMM yyyy HH:mm:ss z", Locale.ENGLISH);
            dataformater.setTimeZone(TimeZone.getTimeZone("GMT"));
            String dateString = dataformater.format(date);
            String sign = sign("GET", dateString, resource);
            conn.setRequestProperty("date", dateString);
            conn.setRequestProperty("Authorization", sign);
            conn.setRequestProperty("Host", endPoint);

            int responseCode = conn.getResponseCode();
            System.out.println("GET Response Code :: " + responseCode);
            if (responseCode == HttpURLConnection.HTTP_OK) { // success
                BufferedReader in = new BufferedReader(new InputStreamReader(
                        conn.getInputStream()));
                String inputLine;
                StringBuffer response = new StringBuffer();

                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();
                return response.toString();
            } else {
                return "{\"stats\":\"404\"}";
            }
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e);
        } finally {

        }
    }
    public static String sign(String httpVerb, String date, String resource) {
        String stringToSign = httpVerb
                + "\n\n\n"
                + date + "\n" + resource;
        try {
            Mac mac = Mac.getInstance("HmacSHA1");
            byte[] keyBytes = secretKey.getBytes("UTF8");
            SecretKeySpec signingKey = new SecretKeySpec(keyBytes, "HmacSHA1");
            mac.init(signingKey);
            byte[] signBytes = mac.doFinal(stringToSign.getBytes("UTF8"));
            String signature = new String(Base64.getEncoder().encode(signBytes));
            return "AWS" + " " + accessKey + ":" + signature;
        } catch (Exception e) {
            throw new RuntimeException("MAC CALC FAILED.");
        }
    }
}
