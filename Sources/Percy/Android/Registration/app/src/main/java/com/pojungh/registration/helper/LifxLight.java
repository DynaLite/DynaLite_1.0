package com.pojungh.registration.helper;

/**
 * Created by pojungh on 4/6/16.
 */
public class LifxLight {
    private String name;
    private String location;
    private String color;
    private boolean isOn;

    public LifxLight(String lightName, String lightLocation, String lightColor, boolean onOff){
        name = lightName;
        location = lightLocation;
        color = lightColor;
        isOn = onOff;
    }

    public String name(){
        return name;
    }

    public String getLocation(){
        return location;
    }

    public String getColor(){
        return color;
    }

    public void setLocation(String lightLocation){
        location = lightLocation;
    }

    public void setColor(String lightColor){
        color = lightColor;
    }

    public boolean isOn(){
        return isOn;
    }

    public void setSwitch(){
        isOn = !isOn;
    }
}