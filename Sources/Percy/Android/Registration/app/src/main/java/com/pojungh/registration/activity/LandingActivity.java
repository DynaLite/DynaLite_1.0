package com.pojungh.registration.activity;

/**
 * Created by pojungh on 4/3/16.
 */

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.pojungh.registration.R;

public class LandingActivity extends Activity {

    private Button btnLogin;
    private Button btnSignup;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_landing);

        btnLogin = (Button)findViewById(R.id.btnLogin_landing);
        btnSignup = (Button) findViewById(R.id.btnLinkToRegisterScreen_landing);

        btnLogin.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(LandingActivity.this, LoginActivity.class);
                startActivity(intent);
                finish();
            }
        });

        btnSignup.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(LandingActivity.this, RegisterActivity.class);
                startActivity(intent);
                finish();
            }
        });
    }
}
