package com.pojungh.registration.activity;

/**
 * Created by pojungh on 3/28/16.
 */
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.pojungh.registration.app.AppConfig;
import com.pojungh.registration.app.AppController;
import com.pojungh.registration.helper.SQLiteHandler;
import com.pojungh.registration.helper.SessionManager;
import com.pojungh.registration.R;

import java.util.HashMap;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.app.Activity;
import android.support.design.widget.NavigationView;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.content.Intent;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.ImageButton;
import android.os.AsyncTask;
import android.widget.Toast;

import com.estimote.sdk.Beacon;
import com.estimote.sdk.BeaconManager;
import com.estimote.sdk.Region;
import com.estimote.sdk.SystemRequirementsChecker;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import com.pojungh.registration.app.TCPClient;
import com.pojungh.registration.helper.LightListAdapter;
import com.pojungh.registration.helper.LifxLight;

import org.json.JSONException;
import org.json.JSONObject;

public class MainActivity extends Activity {

    private SQLiteHandler db;
    private SessionManager session;

    private boolean bulbPower=true;
    private static final Map<String, List<String>> PLACES_BY_BEACONS;
    static {
        Map<String, List<String>> placesByBeacons = new HashMap<>();
        placesByBeacons.put("1148:38184", new ArrayList<String>() {{
            add("blueberry");
        }});
        placesByBeacons.put("13715:45720", new ArrayList<String>() {{
            add("ice");
        }});
        placesByBeacons.put("41903:51220", new ArrayList<String>() {{
            add("mint");
        }});
        PLACES_BY_BEACONS = Collections.unmodifiableMap(placesByBeacons);
    }

    private List<String> placesNearBeacon(Beacon beacon) {
        String beaconKey = String.format("%d:%d", beacon.getMajor(), beacon.getMinor());
        if (PLACES_BY_BEACONS.containsKey(beaconKey)) {
            return PLACES_BY_BEACONS.get(beaconKey);
        }
        return Collections.emptyList();
    }
    private BeaconManager beaconManager;
    private Region region;
    private LightListAdapter adapter;
    private TCPClient tcpClient;
    private ImageButton imgBtn;
    private ArrayList<LifxLight> lights;
    private String CURRENTLOCATION;

    /*public class TCPConnect extends AsyncTask<String, String, TCPClient>{
        @Override
        protected TCPClient doInBackground(String... message){
            tcpClient = new TCPClient(new TCPClient.OnMessageReceived(){
                @Override
                public void messageReceived(String message){
                    publishProgress(message);
                }
            });
            tcpClient.run();

            return null;
        }

        @Override
        protected void onProgressUpdate(String... values){
            super.onProgressUpdate(values);
        }
    }*/

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        imgBtn = (ImageButton)findViewById(R.id.exitButton);
        imgBtn.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                logoutUser();
            }
        });

        adapter = new LightListAdapter(this);
        beaconManager = new BeaconManager(this);
        beaconManager.setRangingListener(new BeaconManager.RangingListener() {
            @Override
            public void onBeaconsDiscovered(Region region, final List<Beacon> list) {
                if (!list.isEmpty()) {
                    Beacon nearestBeacon = list.get(0);
                    List<String> places = placesNearBeacon(nearestBeacon);
                    Log.d("Room", "Nearest places: " + places.get(0));
                    CURRENTLOCATION = places.get(0);
                    updateLocation();
                }

                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        updateLights();
                    }
                });
            }
        });
        region = new Region("ranged region", UUID.fromString("B9407F30-F5F8-466E-AFF9-25556B57FE6D"), null, null);

        // SqLite database handler
        db = new SQLiteHandler(getApplicationContext());

        // session manager
        session = new SessionManager(getApplicationContext());

        if (!session.isLoggedIn()) {
            logoutUser();
        }

        ListView lightList = (ListView)findViewById(R.id.device_list);
        lightList.setAdapter(adapter);


        //new TCPConnect().execute("");
    }

    /**
     * Logging out the user. Will set isLoggedIn flag to false in shared
     * preferences Clears the user data from sqlite users table
     * */
    private void logoutUser() {
        session.setLogin(false);

        db.deleteUsers();

        // Launching the login activity
        Intent intent = new Intent(MainActivity.this, LandingActivity.class);
        startActivity(intent);
        finish();
    }

    @Override
    protected void onResume(){
        super.onResume();
        SystemRequirementsChecker.checkWithDefaultDialogs(this);

        beaconManager.connect(new BeaconManager.ServiceReadyCallback() {
            @Override
            public void onServiceReady() {
                beaconManager.startRanging(region);
            }
        });
    }

    @Override
    protected void onPause(){
        beaconManager.stopRanging(region);

        super.onPause();
    }

    private void updateLights() {
        // Tag used to cancel the request
        String tag_string_req = "req_update_lights";


        StringRequest strReq = new StringRequest(Request.Method.POST,
                AppConfig.URL_GET_BULBS, new Response.Listener<String>() {

            @Override
            public void onResponse(String response) {
                try {
                    JSONObject jObj = new JSONObject(response);
                    boolean error = jObj.getBoolean("error");
                    lights = new ArrayList<LifxLight>();

                    // Check for error node in json
                    if (!error) {
                        int count = jObj.getInt("count");

                        JSONObject light;
                        int currentIndex=0;
                        for(int i=0; i<count; i++){
                            light = jObj.getJSONObject(Integer.toString(i));
                            lights.add(new LifxLight(light.getString("name"), light.getString("location"),
                                    light.getString("color"), light.getInt("isON")==1 ? true : false));
                            if(light.getString("location").equals(CURRENTLOCATION)){
                                currentIndex = i;
                            }
                        }
                        LifxLight currentLight = lights.get(currentIndex);
                        lights.remove(currentIndex);
                        lights.add(0,currentLight);
                        adapter.replaceWith(lights);

                    } else {
                        // Error in login. Get the error message
                        String errorMsg = jObj.getString("error_msg");
                        Toast.makeText(getApplicationContext(),
                                errorMsg, Toast.LENGTH_LONG).show();
                    }
                } catch (JSONException e) {
                    // JSON error
                    e.printStackTrace();
                    Toast.makeText(getApplicationContext(), "Json error: " + e.getMessage(), Toast.LENGTH_LONG).show();
                }

            }
        }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
            }
        });

        // Adding request to request queue
        AppController.getInstance().addToRequestQueue(strReq, tag_string_req);
    }

    private void updateLocation() {
        // Tag used to cancel the request
        String tag_string_req = "req_update_location";


        StringRequest strReq = new StringRequest(Request.Method.POST,
                AppConfig.URL_UPDATE_LOCATION, new Response.Listener<String>() {

            @Override
            public void onResponse(String response) {
                try {
                    JSONObject jObj = new JSONObject(response);
                    boolean error = jObj.getBoolean("error");
                } catch (JSONException e) {
                    // JSON error
                }

            }
        }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
            }
        }){

            @Override
            protected Map<String, String> getParams() {

                // Fetching user details from sqlite
                HashMap<String, String> user = db.getUserDetails();

                // Posting parameters to login url
                Map<String, String> params = new HashMap<String, String>();
                params.put("id", user.get("id"));
                params.put("location", CURRENTLOCATION);

                return params;
            }

        };

        // Adding request to request queue
        AppController.getInstance().addToRequestQueue(strReq, tag_string_req);
    }

}