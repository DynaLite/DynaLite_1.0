package com.pojungh.registration.helper;

import android.content.Context;
import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.pojungh.registration.app.AppConfig;
import com.pojungh.registration.app.AppController;
import com.pojungh.registration.helper.ColorPickerDialog.OnColorSelectedListener;

import com.estimote.sdk.Beacon;
import com.estimote.sdk.Utils;
import com.pojungh.registration.R;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

import android.content.Context;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by pojungh on 4/6/16.
 */
public class LightListAdapter extends BaseAdapter {
    private Context context;
    private ArrayList<LifxLight> lights;
    private LayoutInflater inflater;
    private final LifxLight currentLight;

    public LightListAdapter(Context parentContext) {
        this.inflater = LayoutInflater.from(parentContext);
        this.lights = new ArrayList<>();
        context = parentContext;
        currentLight = new LifxLight("null", "null", "null", false);
    }

    public void replaceWith(Collection<LifxLight> newLights) {
        this.lights.clear();
        this.lights.addAll(newLights);
        notifyDataSetChanged();
    }

    @Override
    public int getCount() {
        return lights.size();
    }

    @Override
    public LifxLight getItem(int position) {
        return lights.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View view, ViewGroup parent) {
        view = inflateIfRequired(view, position, parent);
        bind(getItem(position), view);
        return view;
    }

    private void bind(LifxLight light, View view) {
        ViewHolder holder = (ViewHolder) view.getTag();
        if(light.name().equals(lights.get(0).name())){
            holder.imagePerson.setVisibility(View.VISIBLE);
        }
        else{
            holder.imagePerson.setVisibility(View.INVISIBLE);
        }
        holder.nameTextView.setText("Name: "+light.name());
        holder.whereTextView.setText("Location: " + light.getLocation());
        holder.lightItem.setBackgroundColor(Color.parseColor(light.isOn() ? light.getColor() : "#383838"));
        if(light.name().equals(lights.get(0).name())){
            currentLight.setLocation(light.getLocation());
            holder.lightItem.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    int initialColor = Color.WHITE;

                    ColorPickerDialog colorPickerDialog = new ColorPickerDialog(context, initialColor, new OnColorSelectedListener() {

                        @Override
                        public void onColorSelected(int color) {
                            String hexColor = String.format("#%06X", (0xFFFFFF & color));
                            currentLight.setColor(hexColor);
                            updateColorToServer();
                        }

                    });
                    colorPickerDialog.show();
                }
            });
        }else{
            holder.lightItem.setOnClickListener(null);
        }
        holder.imageView.setImageResource(light.isOn()? R.drawable.bulb : R.drawable.bulb_black);
    }

    private View inflateIfRequired(View view, int position, ViewGroup parent) {
        if (view == null) {
            view = inflater.inflate(R.layout.lifx_item, null);
            view.setTag(new ViewHolder(view));
        }
        return view;
    }

    static class ViewHolder {
        final ImageView imagePerson;
        final ImageView imageView;
        final TextView nameTextView;
        final TextView whereTextView;
        final LinearLayout lightItem;

        ViewHolder(View view) {
            imagePerson = (ImageView) view.findViewWithTag("imgPerson");
            imageView = (ImageView) view.findViewWithTag("imgLifx");
            nameTextView = (TextView) view.findViewWithTag("lifxName");
            whereTextView = (TextView) view.findViewWithTag("lifxWhere");
            lightItem = (LinearLayout) view.findViewById(R.id.lightItem);
        }
    }

    private void updateColorToServer() {
        // Tag used to cancel the request
        String tag_string_req = "req_update_color";


        StringRequest strReq = new StringRequest(Request.Method.POST,
                AppConfig.URL_UPDATE_COLOR, new Response.Listener<String>() {

            @Override
            public void onResponse(String response) {
            }
        }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
            }
        }){

            @Override
            protected Map<String, String> getParams() {
                // Posting parameters to login url
                Map<String, String> params = new HashMap<String, String>();
                params.put("location", currentLight.getLocation());
                params.put("color", currentLight.getColor());

                return params;
            }

        };

        // Adding request to request queue
        AppController.getInstance().addToRequestQueue(strReq, tag_string_req);
    }
}
