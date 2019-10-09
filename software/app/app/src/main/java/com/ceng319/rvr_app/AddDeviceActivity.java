package com.ceng319.rvr_app;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;


import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import com.google.android.gms.vision.CameraSource;
import com.google.android.gms.vision.barcode.BarcodeDetector;
import com.google.android.gms.vision.barcode.Barcode;

/*
Resources:
    https://developers.google.com/vision/android/barcodes-overview
    https://developers.google.com/android/reference/com/google/android/gms/vision/barcode/BarcodeDetector
    https://github.com/googlesamples/android-vision/blob/master/visionSamples/barcode-reader/app/src/main/java/com/google/android/gms/samples/vision/barcodereader/BarcodeCaptureActivity.java
*/


public class AddDeviceActivity extends AppCompatActivity {
    private static final int CAMERA_PERMISSION_REQUEST_CODE = 1;
    private static final String TAG = "RVR_app";

    private CameraSource mCameraSource;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_adddevice);


        //Check for camera permission
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
            setupCamera();
        }
        else {
            requestCameraPermission();
        }

    }

    void setupCamera() {
        Context context = getApplicationContext();

        //Create a BarcodeDetector
        BarcodeDetector detector = new BarcodeDetector.Builder(context).build();


        if (!detector.isOperational()) {
            //Libraries will be downloaded the first time the app is run
            //It may take some time, so check to make sure the barcodeDetector is operational
            Log.w(TAG, "BarcodeDetector dependenceis not yet loaded");

            //TODO: Add check for low storage, which may prevent installation of dependencies
        }

        CameraSource.Builder builder = new CameraSource.Builder(getApplicationContext(), detector)
                .setFacing(CameraSource.CAMERA_FACING_BACK)
                //.setRequestedPreviewSize()
                .setRequestedFps(20);

        //TODO: Make sure auto focus is available and set it up. May need min SDK Ice cream sandwich

        mCameraSource = builder.build();
    }

    //If camera permissions are not granted, request them
    void requestCameraPermission() {

        String[] permissions = {Manifest.permission.CAMERA};
        ActivityCompat.requestPermissions(this, permissions, CAMERA_PERMISSION_REQUEST_CODE);

    }

    //Handle the result of the camera permission request
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        if (requestCode == CAMERA_PERMISSION_REQUEST_CODE) {
            if (grantResults.length != 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                setupCamera();
            }
        }
    }
}
