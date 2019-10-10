package com.ceng319.rvr_app;

import android.Manifest;
import android.app.Dialog;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;


import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GoogleApiAvailability;
import com.google.android.gms.vision.CameraSource;
import com.google.android.gms.vision.MultiProcessor;
import com.google.android.gms.vision.barcode.BarcodeDetector;
import com.google.android.gms.vision.barcode.Barcode;

import java.io.IOException;
import java.util.List;

/*
Resources:
    https://developers.google.com/vision/android/barcodes-overview
    https://developers.google.com/android/reference/com/google/android/gms/vision/barcode/BarcodeDetector
    https://github.com/googlesamples/android-vision/blob/master/visionSamples/barcode-reader/app/src/main/java/com/google/android/gms/samples/vision/barcodereader/BarcodeCaptureActivity.java
*/


public class AddDeviceActivity extends AppCompatActivity implements BarcodeGraphicTracker.BarcodeUpdateListener{
    private static final int CAMERA_PERMISSION_REQUEST_CODE = 1;
    // intent request code to handle updating play services if needed.
    private static final int RC_HANDLE_GMS = 9001;
    private static final String TAG = "RVR_app";

    private CameraSource mCameraSource = null;
    private GraphicOverlay<BarcodeGraphic> mGraphicOverlay;
    private CameraSourcePreview mPreview = null;
    Button captureButton;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_adddevice);

        mPreview = findViewById(R.id.preview);
        mGraphicOverlay = findViewById(R.id.graphicOverlay);


        //Check for camera permission
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
            setupCamera();
        }
        else {
            requestCameraPermission();
        }

        captureButton = findViewById(R.id.captureButton);
        captureButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Barcode barcode;
                if ((barcode = getBarcode()) == null) {
                    Toast.makeText(getApplicationContext(), "No barcode detected", Toast.LENGTH_SHORT).show();
                }
                else {
                    Toast.makeText(getApplicationContext(), barcode.displayValue, Toast.LENGTH_SHORT).show();
                }
            }
        });

    }

    void setupCamera() {
        Context context = getApplicationContext();

        //Create a BarcodeDetector
        BarcodeDetector detector = new BarcodeDetector.Builder(context).setBarcodeFormats(Barcode.QR_CODE).build();

        BarcodeTrackerFactory barcodeFactory = new BarcodeTrackerFactory(mGraphicOverlay, this);
        detector.setProcessor(new MultiProcessor.Builder<>(barcodeFactory).build());

        if (!detector.isOperational()) {
            //Libraries will be downloaded the first time the app is run
            //It may take some time, so check to make sure the barcodeDetector is operational
            Log.w(TAG, "BarcodeDetector dependenceis not yet loaded");

            //TODO: Add check for low storage, which may prevent installation of dependencies
        }

        CameraSource.Builder builder = new CameraSource.Builder(getApplicationContext(), detector)
                .setFacing(CameraSource.CAMERA_FACING_BACK)
                .setRequestedPreviewSize(1920,1080)
                .setRequestedFps(15);

        //TODO: Make sure auto focus is available and set it up. May need min SDK Ice cream sandwich

        mCameraSource = builder.build();

    }

    //Gets the barcode, returns null if no barcode
    Barcode getBarcode() {
        Barcode barcode = null;
        List<BarcodeGraphic> barcodeList = mGraphicOverlay.getGraphics();

        if (!barcodeList.isEmpty()) {
            Log.d(TAG, "Barcode list is not empty");
            barcode = barcodeList.get(0).getBarcode();
        }

        return barcode;
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


    /**
     * Restarts the camera.
     */
    @Override
    protected void onResume() {
        super.onResume();
        startCameraSource();
    }

    /**
     * Stops the camera.
     */
    @Override
    protected void onPause() {
        super.onPause();
        if (mPreview != null) {
            mPreview.stop();
        }
    }

    /**
     * Releases the resources associated with the camera source, the associated detectors, and the
     * rest of the processing pipeline.
     */
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (mPreview != null) {
            mPreview.release();
        }
    }

    private void startCameraSource() throws SecurityException {
        // check that the device has play services available.
        int code = GoogleApiAvailability.getInstance().isGooglePlayServicesAvailable(
                getApplicationContext());
        if (code != ConnectionResult.SUCCESS) {
            Dialog dlg =
                    GoogleApiAvailability.getInstance().getErrorDialog(this, code, RC_HANDLE_GMS);
            dlg.show();
        }

        if (mCameraSource != null) {
            try {
                mPreview.start(mCameraSource, mGraphicOverlay);
            } catch (IOException e) {
                Log.e(TAG, "Unable to start camera source.", e);
                mCameraSource.release();
                mCameraSource = null;
            }
        }
    }

    //TODO: Method is not called. Called from onNewItem() in BarcodeGraphicTracker, which is not called
    @Override
    public void onBarcodeDetected(Barcode barcode) {
        Log.d(TAG,"Barcode detected");
    }
}
