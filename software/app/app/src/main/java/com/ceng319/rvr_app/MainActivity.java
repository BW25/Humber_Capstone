package com.ceng319.rvr_app;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    private ImageView scanIcon;
    private ImageView historyIcon;
    private ImageView lookupIcon;
    private ImageView settingsIcon;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        //Replace loading screen
        setTheme(R.style.AppTheme);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        setupMenuBar();
    }

    //This method is a template to interface with the menu bar
    //Each section sets up one of the four buttons
    //TODO: Remove the button for the current activity: We don't want the activity to have a button to go to itself
    void setupMenuBar() {
        scanIcon = findViewById(R.id.scanIcon);
        scanIcon.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), ScanActivity.class);
                startActivity(intent);
            }
        });

        historyIcon = findViewById(R.id.historyIcon);
        historyIcon.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), HistoryActivity.class);
                startActivity(intent);
            }
        });

        //TODO: Some activities have yet to be created
        //TODO: If you name them something different, be sure to change the name here
        lookupIcon = findViewById(R.id.lookupIcon);
        lookupIcon.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), AddDeviceActivity.class);
                startActivity(intent);
            }
        });
/*
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
