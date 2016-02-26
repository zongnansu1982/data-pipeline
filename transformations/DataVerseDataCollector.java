package edu.ucsd.domi.dataverse;

import java.io.IOException;
import java.util.ArrayList;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.ParseException;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.utils.URLEncodedUtils;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;


/**
 * 
 * @author nansu
 *
 */
public class DataVerseDataCollector {

	public static void main(String[] args) throws ClientProtocolException, ParseException, IOException, JSONException {
		// TODO Auto-generated method stub
		DataVerseDataCollector collector=new DataVerseDataCollector();
		collector.search();
//		collector.access();
	}

	
	public void search()
			throws ClientProtocolException, IOException, ParseException,
			JSONException {
		HttpClient httpclient = new DefaultHttpClient();
		ArrayList<NameValuePair> params = new ArrayList<NameValuePair>();

		/**
		 * To Sunil:
		 * 
		 * 1. transform the unannotated codes into py codes to extract jason files in each request (1000 files max).
		 * 
		 * 2. iterate step 1 for (60291/1000 +1 ) times
		 * 
		 * 3. for each file extracted, separate them into sub jason files, where each one for each data set
		 * 
		 * 4. after all, you will get 60291 jason fiels for all the 60291 data sets.
		 * 
		 *  @author nansu
		 */
		
		params.add(new BasicNameValuePair("q", "*"));
		params.add(new BasicNameValuePair("type", "dataset"));
			
		
//		params.add(new BasicNameValuePair("q", "*"));
//		params.add(new BasicNameValuePair("type", "dataset"));
//		params.add(new BasicNameValuePair("subtree", "WASL"));
//		params.add(new BasicNameValuePair("fq", "subject:Medicine, Health and Life Sciences"));

		
		
		
//		params.add(new BasicNameValuePair("q", "*"));
//		params.add(new BasicNameValuePair("type", "file"));
//		params.add(new BasicNameValuePair("fq", "global_id:doi:10.7910/DVN/BM8FSC"));
		
		params.add(new BasicNameValuePair("key", "5a33bbc7-8744-4c51-b737-c8079b326d40"));
		
		String serviceURL = "https://dataverse.harvard.edu/api/search";
//		String serviceURL = "https://apitest.dataverse.org/api/search";
		String url = serviceURL + "?" + URLEncodedUtils.format(params, "UTF-8");
		System.out.println(url);
		HttpResponse response = httpclient.execute(new HttpGet(url));

		String string = EntityUtils.toString(response.getEntity());
		System.out.println(string);

	}
	
	public void access()
			throws ClientProtocolException, IOException, ParseException,
			JSONException {
		HttpClient httpclient = new DefaultHttpClient();
		ArrayList<NameValuePair> params = new ArrayList<NameValuePair>();
		params.add(new BasicNameValuePair("key", "5a33bbc7-8744-4c51-b737-c8079b326d40"));
		
		String serviceURL = "https://dataverse.harvard.edu/api/files/hdl:1902.29/CD-0077";
//		String serviceURL = "https://apitest.dataverse.org/api/search";
		String url = serviceURL + "?" + URLEncodedUtils.format(params, "UTF-8");
		System.out.println(url);
		HttpResponse response = httpclient.execute(new HttpGet(url));

		String string = EntityUtils.toString(response.getEntity());
		System.out.println(string);

//		JSONObject obj = null;
//
//		obj = new JSONObject(string);
//
//		// System.out.println(status);
//
//		JSONArray arr = null;
//
//		arr = obj.optJSONArray("result");
//		
//		
//		
//		return list;
	}
	
}
