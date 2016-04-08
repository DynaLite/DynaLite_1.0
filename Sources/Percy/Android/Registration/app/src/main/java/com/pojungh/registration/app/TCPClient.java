package com.pojungh.registration.app;

/**
 * Created by pojungh on 4/3/16.
 */
import android.util.Log;
import java.io.*;
import java.net.InetAddress;
import java.net.Socket;

public class TCPClient {

    private String serverMessage;
    public String SERVERIP = "35.2.68.86";
    public int SERVERPORT = 12345;
    private OnMessageReceived messageListener=null;
    private boolean isRun=false;

    PrintWriter out;
    BufferedReader in;

    public interface OnMessageReceived{
        public void messageReceived(String message);
    }

    public TCPClient(OnMessageReceived listener){
        messageListener = listener;
    }

    public void sendMessage(String message){
        if(out!=null && !out.checkError()){
            out.println(message);
            out.flush();
        }
    }
    public void setIPPort(String IP, int port){
        SERVERIP = IP;
        SERVERPORT = port;
    }
    public String getIP(){
        return SERVERIP;
    }
    public int getPORT(){
        return SERVERPORT;
    }

    public void stopClient(){
        isRun = false;
    }

    public void run(){
        isRun = true;

        try{
            InetAddress serverAddr = InetAddress.getByName(SERVERIP);

            Log.e("TCP Client", "C: Connecting...");

            Socket socket = new Socket(serverAddr, SERVERPORT);

            try{
                out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);
                Log.e("TCP Client", "C: Sent.");
                Log.e("TCP Client", "C: Done.");

                in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                while(isRun){
                    serverMessage = in.readLine();
                    if(serverMessage!=null && messageListener!=null){
                        messageListener.messageReceived(serverMessage);
                    }
                    serverMessage = null;
                }

            }catch (Exception e){
                Log.e("TCP", "S: Error", e);
            }finally {
                socket.close();
            }

        }catch (Exception e){
            Log.e("TCP", "C: Error", e);
        }
    }
}

