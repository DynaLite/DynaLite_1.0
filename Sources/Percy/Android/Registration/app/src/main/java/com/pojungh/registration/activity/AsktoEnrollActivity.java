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

public class AsktoEnrollActivity extends Activity {

    private Button btnEnroll;
    private Button btnSkip;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_toenroll_or_not);

        btnEnroll = (Button)findViewById(R.id.btnEnroll);
        btnSkip = (Button) findViewById(R.id.btnSkip);

        btnSkip.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(AsktoEnrollActivity.this, MainActivity.class);
                startActivity(intent);
                finish();
            }
        });

        btnEnroll.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(AsktoEnrollActivity.this, AudioActivity.class);
                startActivity(intent);
                finish();
            }
        });
    }
}
