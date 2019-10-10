package com.ceng319.rvr_app;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class ScanActivity extends AppCompatActivity {
    private ImageView historyIcon;
    private ImageView lookupIcon;
    private ImageView settingsIcon;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        //Replace loading screen
        setTheme(R.style.AppTheme);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_scan);
        setupMenuBar();


    }

    void setupMenuBar() {
        historyIcon = findViewById(R.id.historyIcon);
        historyIcon.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), HistoryActivity.class);
                startActivity(intent);
            }
        });
        /*
        lookupIcon = findViewById(R.id.lookupIcon);
        lookupIcon.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), LookupActivity.class);
                startActivity(intent);
            }
        });

        settingsIcon = findViewById(R.id.settingsIcon);
        settingsIcon.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), SettingsActivity.class);
                startActivity(intent);
            }
        });*/
    }
}
