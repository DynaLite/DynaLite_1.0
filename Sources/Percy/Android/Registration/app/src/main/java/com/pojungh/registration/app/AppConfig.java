package com.pojungh.registration.app;

/**
 * Created by pojungh on 3/28/16.
 */
public class AppConfig {
    private static String SERVER_IP = "http://172.20.10.2/";

    // Server user login url
    public static String URL_LOGIN = SERVER_IP+"DynalitePHPServer/login.php";

    // Server user register url
    public static String URL_REGISTER = SERVER_IP+"DynalitePHPServer/register.php";

    public static String URL_KEY_UPDATE = SERVER_IP+"DynalitePHPServer/updateKey.php";

    public static String URL_GET_BULBS = SERVER_IP+"DynalitePHPServer/getBulbs.php";

    public static String URL_UPDATE_LOCATION = SERVER_IP+"DynalitePHPServer/updateLocation.php";

    public static String URL_UPDATE_COLOR = SERVER_IP+"DynalitePHPServer/updateColor.php";
}
