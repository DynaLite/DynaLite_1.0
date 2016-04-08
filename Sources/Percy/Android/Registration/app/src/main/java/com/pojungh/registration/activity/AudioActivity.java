package com.pojungh.registration.activity;

/**
 * Created by pojungh on 4/3/16.
 */
//import android.support.v7.app.AppCompatActivity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.pojungh.registration.R;
import com.pojungh.registration.app.AppConfig;
import com.pojungh.registration.app.AppController;
import com.pojungh.registration.helper.SQLiteHandler;
import com.pojungh.registration.helper.SessionManager;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

import android.app.Activity;
import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
//import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import java.net.URL;
import javax.net.ssl.HttpsURLConnection;
import java.io.DataOutputStream;
import java.util.HashMap;
import java.util.Map;

import org.json.JSONException;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class AudioActivity extends Activity {
    private static final int RECORDER_BPP = 16;
    private static final String AUDIO_RECORDER_FILE_EXT_WAV = ".wav";
    private static final String AUDIO_RECORDER_FOLDER = "AudioRecorder";
    private static final String AUDIO_RECORDER_TEMP_FILE = "record_temp.raw";
    private static final int RECORDER_SAMPLERATE = 16000;
    private static final int RECORDER_CHANNELS = AudioFormat.CHANNEL_IN_MONO;
    private static final int RECORDER_AUDIO_ENCODING = AudioFormat.ENCODING_PCM_16BIT;

    private AudioRecord recorder = null;
    private int bufferSize = 0;
    private Thread recordingThread = null;
    private boolean isRecording = false;
    private String wavFilename;
    private String profileID = null;
    private SQLiteHandler db;


    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_audiorecord);

        db = new SQLiteHandler(getApplicationContext());


        setButtonHandlers();
        enableButtons(false);
        findViewById(R.id.btnSend).setEnabled(false);
        findViewById(R.id.btnStop).setVisibility(View.GONE);

        bufferSize = AudioRecord.getMinBufferSize(RECORDER_SAMPLERATE,
                AudioFormat.CHANNEL_IN_MONO,
                AudioFormat.ENCODING_PCM_16BIT);
    }

    private void setButtonHandlers() {
        ((Button)findViewById(R.id.btnStart)).setOnClickListener(btnClick);
        ((Button)findViewById(R.id.btnStop)).setOnClickListener(btnClick);
        ((Button)findViewById(R.id.btnSend)).setOnClickListener(btnClick);
        ((Button)findViewById(R.id.btnToMain)).setOnClickListener(btnClick);
    }

    private void enableButton(int id,boolean isEnable){
        ((Button)findViewById(id)).setEnabled(isEnable);
    }

    private void enableButtons(boolean isRecording) {
        enableButton(R.id.btnStart,!isRecording);
        enableButton(R.id.btnStop,isRecording);
    }

    private String getFilename(){
        String filepath = Environment.getExternalStorageDirectory().getPath();
        File file = new File(filepath,AUDIO_RECORDER_FOLDER);

        if(!file.exists()){
            file.mkdirs();
        }

        return (file.getAbsolutePath() + "/" + System.currentTimeMillis() + AUDIO_RECORDER_FILE_EXT_WAV);
    }

    private String getTempFilename(){
        String filepath = Environment.getExternalStorageDirectory().getPath();
        File file = new File(filepath,AUDIO_RECORDER_FOLDER);

        if(!file.exists()){
            file.mkdirs();
        }

        File tempFile = new File(filepath,AUDIO_RECORDER_TEMP_FILE);

        if(tempFile.exists())
            tempFile.delete();

        return (file.getAbsolutePath() + "/" + AUDIO_RECORDER_TEMP_FILE);
    }

    private void startRecording(){
        recorder = new AudioRecord(MediaRecorder.AudioSource.MIC,
                RECORDER_SAMPLERATE, RECORDER_CHANNELS,RECORDER_AUDIO_ENCODING, bufferSize);

        int i = recorder.getState();
        if(i==1)
            recorder.startRecording();

        isRecording = true;

        recordingThread = new Thread(new Runnable() {

            @Override
            public void run() {
                writeAudioDataToFile();
            }
        },"AudioRecorder Thread");

        recordingThread.start();
    }

    private void writeAudioDataToFile(){
        byte data[] = new byte[bufferSize];
        String filename = getTempFilename();
        FileOutputStream os = null;

        try {
            os = new FileOutputStream(filename);
        } catch (FileNotFoundException e) {
// TODO Auto-generated catch block
            e.printStackTrace();
        }

        int read = 0;

        if(null != os){
            while(isRecording){
                read = recorder.read(data, 0, bufferSize);

                if(AudioRecord.ERROR_INVALID_OPERATION != read){
                    try {
                        os.write(data);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }

            try {
                os.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private void stopRecording(){
        if(null != recorder){
            isRecording = false;

            int i = recorder.getState();
            if(i==1)
                recorder.stop();
            recorder.release();

            recorder = null;
            recordingThread = null;
        }

        copyWaveFile(getTempFilename(),getFilename());
        deleteTempFile();
    }

    private void deleteTempFile() {
        File file = new File(getTempFilename());

        file.delete();
    }

    private void copyWaveFile(String inFilename,String outFilename){
        FileInputStream in = null;
        FileOutputStream out = null;
        long totalAudioLen = 0;
        long totalDataLen = totalAudioLen + 36;
        long longSampleRate = RECORDER_SAMPLERATE;
        int channels = 1;
        long byteRate = RECORDER_BPP * RECORDER_SAMPLERATE * channels/8;

        byte[] data = new byte[bufferSize];

        try {
            in = new FileInputStream(inFilename);
            out = new FileOutputStream(outFilename);
            totalAudioLen = in.getChannel().size();
            totalDataLen = totalAudioLen + 36;



            WriteWaveFileHeader(out, totalAudioLen, totalDataLen,
                    longSampleRate, channels, byteRate);

            while(in.read(data) != -1){
                out.write(data);
            }

            in.close();
            out.close();
            wavFilename = outFilename;
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void WriteWaveFileHeader(
            FileOutputStream out, long totalAudioLen,
            long totalDataLen, long longSampleRate, int channels,
            long byteRate) throws IOException {

        byte[] header = new byte[44];

        header[0] = 'R'; // RIFF/WAVE header
        header[1] = 'I';
        header[2] = 'F';
        header[3] = 'F';
        header[4] = (byte) (totalDataLen & 0xff);
        header[5] = (byte) ((totalDataLen >> 8) & 0xff);
        header[6] = (byte) ((totalDataLen >> 16) & 0xff);
        header[7] = (byte) ((totalDataLen >> 24) & 0xff);
        header[8] = 'W';
        header[9] = 'A';
        header[10] = 'V';
        header[11] = 'E';
        header[12] = 'f'; // 'fmt ' chunk
        header[13] = 'm';
        header[14] = 't';
        header[15] = ' ';
        header[16] = 16; // 4 bytes: size of 'fmt ' chunk
        header[17] = 0;
        header[18] = 0;
        header[19] = 0;
        header[20] = 1; // format = 1
        header[21] = 0;
        header[22] = (byte) channels;
        header[23] = 0;
        header[24] = (byte) (longSampleRate & 0xff);
        header[25] = (byte) ((longSampleRate >> 8) & 0xff);
        header[26] = (byte) ((longSampleRate >> 16) & 0xff);
        header[27] = (byte) ((longSampleRate >> 24) & 0xff);
        header[28] = (byte) (byteRate & 0xff);
        header[29] = (byte) ((byteRate >> 8) & 0xff);
        header[30] = (byte) ((byteRate >> 16) & 0xff);
        header[31] = (byte) ((byteRate >> 24) & 0xff);
        header[32] = (byte) (2 * 16 / 8); // block align
        header[33] = 0;
        header[34] = RECORDER_BPP; // bits per sample
        header[35] = 0;
        header[36] = 'd';
        header[37] = 'a';
        header[38] = 't';
        header[39] = 'a';
        header[40] = (byte) (totalAudioLen & 0xff);
        header[41] = (byte) ((totalAudioLen >> 8) & 0xff);
        header[42] = (byte) ((totalAudioLen >> 16) & 0xff);
        header[43] = (byte) ((totalAudioLen >> 24) & 0xff);

        out.write(header, 0, 44);
    }

    private View.OnClickListener btnClick = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            switch(v.getId()){
                case R.id.btnStart:{
                    enableButtons(true);
                    findViewById(R.id.btnStart).setVisibility(View.GONE);
                    findViewById(R.id.btnStop).setVisibility(View.VISIBLE);

                    startRecording();

                    break;
                }
                case R.id.btnStop:{
                    enableButtons(false);
                    findViewById(R.id.btnStop).setVisibility(View.GONE);
                    findViewById(R.id.btnStart).setVisibility(View.VISIBLE);
                    findViewById(R.id.btnSend).setEnabled(true);

                    stopRecording();

                    break;
                }
                case R.id.btnToMain:{
                    Intent intent = new Intent(AudioActivity.this, MainActivity.class);
                    startActivity(intent);
                    finish();

                    break;
                }
                case R.id.btnSend:{
                    if(profileID == null) {
                        try {
                            String url = "https://api.projectoxford.ai/spid/v1.0/identificationProfiles";
                            String subsKey = "03ecc28131aa421a97552b830100135f";
                            URL obj = new URL(url);
                            HttpsURLConnection conn = (HttpsURLConnection) obj.openConnection();

                            conn.setRequestMethod("POST");
                            conn.setRequestProperty("Content-Type", "application/json");
                            conn.setRequestProperty("Ocp-Apim-Subscription-Key", subsKey);

                            conn.setDoOutput(true);
                            DataOutputStream outStream = new DataOutputStream(conn.getOutputStream());
                            JSONObject jObj = new JSONObject();
                            jObj.put("locale", "en-us");

                            outStream.writeBytes(jObj.toJSONString());
                            outStream.flush();
                            outStream.close();

                            int responseCode = conn.getResponseCode();
                            String responseMsg = conn.getResponseMessage();

                            if (responseCode == 200) {
                                JSONParser parser = new JSONParser();
                                jObj = (JSONObject) parser.parse(responseMsg);
                                profileID = (String) jObj.get("identificationProfileId");

                                try {
                                    url = "https://api.projectoxford.ai/spid/v1.0/identificationProfiles/" + profileID + "/enroll";
                                    subsKey = "03ecc28131aa421a97552b830100135f";
                                    obj = new URL(url);
                                    conn = (HttpsURLConnection) obj.openConnection();

                                    conn.setRequestMethod("POST");
                                    conn.setRequestProperty("Content-Type", "multipart/form-data");
                                    conn.setRequestProperty("Ocp-Apim-Subscription-Key", subsKey);

                                    conn.setDoOutput(true);
                                    outStream = new DataOutputStream(conn.getOutputStream());
                                    byte[] wavData = new byte[bufferSize];
                                    FileInputStream inStream = new FileInputStream(wavFilename);
                                    while (inStream.read(wavData) != -1) {
                                        outStream.write(wavData);
                                    }
                                    outStream.flush();
                                    outStream.close();

                                    responseCode = conn.getResponseCode();
                                    if (responseCode == 202) {
                                        updateKey(profileID);
                                        Intent intent = new Intent(AudioActivity.this, MainActivity.class);
                                        startActivity(intent);
                                        finish();
                                    } else {
                                        Toast.makeText(getApplicationContext(), "enroll failed", Toast.LENGTH_LONG).show();
                                    }

                                } catch (Exception e) {
                                    System.out.println(e.getMessage());
                                } finally {
                                    conn.disconnect();
                                }
                            } else {
                                Toast.makeText(getApplicationContext(), responseMsg, Toast.LENGTH_LONG).show();
                            }
                        } catch (Exception e) {
                            System.out.println(e.getMessage());
                        }
                    }
                    else{
                        try {
                                String url = "https://api.projectoxford.ai/spid/v1.0/identificationProfiles/" + profileID + "/enroll";
                                String subsKey = "03ecc28131aa421a97552b830100135f";
                                URL obj = new URL(url);
                                HttpsURLConnection conn = (HttpsURLConnection) obj.openConnection();

                                conn.setRequestMethod("POST");
                                conn.setRequestProperty("Content-Type", "multipart/form-data");
                                conn.setRequestProperty("Ocp-Apim-Subscription-Key", subsKey);

                                conn.setDoOutput(true);
                                DataOutputStream outStream = new DataOutputStream(conn.getOutputStream());
                                byte[] wavData = new byte[bufferSize];
                                FileInputStream inStream = new FileInputStream(wavFilename);
                                while (inStream.read(wavData) != -1) {
                                    outStream.write(wavData);
                                }
                                outStream.flush();
                                outStream.close();

                                int responseCode = conn.getResponseCode();
                                if (responseCode == 202) {
                                    updateKey(profileID);
                                    Intent intent = new Intent(AudioActivity.this, MainActivity.class);
                                    startActivity(intent);
                                    finish();
                                }
                                else{
                                    Toast.makeText(getApplicationContext(), "enroll failed", Toast.LENGTH_LONG).show();
                                }
                            } catch (Exception e) {
                                System.out.println(e.getMessage());
                            }
                    }

                    break;
                }

            }
        }
    };

    private void updateKey(final String key) {
        // Tag used to cancel the request
        String tag_string_req = "req_update";
        final ProgressDialog pDialog = new ProgressDialog(this);
        pDialog.setMessage("Updating Project Oxford ID to server...");
        pDialog.show();

        StringRequest strReq = new StringRequest(Request.Method.POST,
                AppConfig.URL_KEY_UPDATE, new Response.Listener<String>() {

            @Override
            public void onResponse(String response) {
                Log.d(AudioActivity.class.getSimpleName(), "Update Response: " + response.toString());
                pDialog.dismiss();

                try {
                    org.json.JSONObject jObj = new org.json.JSONObject(response);
                    boolean error = jObj.getBoolean("error");

                    // Check for error node in json
                    if (!error) {
                        // updated
                        Toast.makeText(getApplicationContext(), "update success", Toast.LENGTH_LONG).show();


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
                Log.e(AudioActivity.class.getSimpleName(), "update Error: " + error.getMessage());
                Toast.makeText(getApplicationContext(),
                        error.getMessage(), Toast.LENGTH_LONG).show();
                pDialog.dismiss();
            }
        }) {

            @Override
            protected Map<String, String> getParams() {

                HashMap<String, String> user = db.getUserDetails();

                // Posting parameters to login url
                Map<String, String> params = new HashMap<String, String>();
                params.put("email", user.get("email"));
                params.put("key", key);

                return params;
            }

        };

        // Adding request to request queue
        AppController.getInstance().addToRequestQueue(strReq, tag_string_req);
    }
}
