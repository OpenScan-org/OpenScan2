# ADR: Design and Implementation of OpenScan API

## Status

Accepted

## Context

The OpenScan Meanwhile project requires a robust API to facilitate communication between the front-end interface and the underlying hardware components, including the camera and motors. The API must support various operations such as taking photos, controlling the camera settings, managing system states (shutdown and reboot), and operating motors, as well as feedback to the user.

## Decision

We will implement a RESTful API using Flask and Flask-RESTX, structured to provide clear and organized access to system functionalities. The API will be versioned and will include the following namespaces:

1. **System Operations (`/v1/system`)**:
   - **GET `/status`**: Retrieve the current status of the system, including elapsed time and estimated time remaining for ongoing operations.
   - **GET `/shutdown`**: Initiate a shutdown of the Raspberry Pi.
   - **GET `/reboot`**: Initiate a reboot of the Raspberry Pi.
   - **GET `/ringlight`**: Control the state of the ringlight (on/off).

![System](../img/Openscan%20Api%20System.png)

2. **Camera Operations (`/v1/camera`)**:
   - **GET `/picam2_init`**: Initialize the camera and set up configurations.
   - **GET `/picam2_take_photo`**: Capture a photo, process it, and save it to a specified location.
   - **GET `/picam2_take_photo_raw`**: Capture a photo and return it in raw format.
   - **GET `/picam2_focus`**: Set the focus of the camera to a specified position.
   - **GET `/picam2_af`**: Trigger auto-focus functionality.
   - **GET `/picam2_exposure`**: Set the camera's exposure time.
   - **GET `/picam2_contrast`**: Adjust the camera's contrast settings.
   - **GET `/picam2_saturation`**: Adjust the camera's saturation settings.
   - **GET `/picam2_switch_mode`**: Switch between different camera modes.
   - **GET `/picam2_show_mode`**: Retrieve the current camera mode.

![Camera](../img/Openscan%20Api%20Camera.png)

3. **Motor Operations (`/v1/motor`)**:
   - **GET `/motor_run`**: Control a specified motor, allowing for angle adjustments and endstop configurations.

![Motor](../img/Openscan%20Api%20Motor.png)
## Consequences

### Positive

1. **Modular Design**: The API is organized into namespaces, making it easy to understand and extend in the future.
2. **Versioning**: The API is versioned (`/v1`), allowing for backward compatibility as new features are added in future versions.
3. **Clear Documentation**: Each endpoint is documented with parameters and expected responses, facilitating easier integration and usage.


### Negative

1. **Complexity**: The introduction of multiple namespaces and endpoints may increase the complexity of the codebase.
2. **Error Handling**: While basic error handling is implemented, more comprehensive error management may be required as the API evolves.
3. **Performance**: Depending on the implementation of the underlying hardware interactions, performance may vary, especially during high-load operations.

## Implementation

The API is implemented using Flask and Flask-RESTX, with the following key components:

- **Flask**: A lightweight WSGI web application framework for Python.
- **Flask-RESTX**: An extension for Flask that simplifies the creation of RESTful APIs.
- **Picamera2**: A library for controlling the Raspberry Pi camera.
- **GPIO**: A library for controlling the Raspberry Pi's GPIO pins.

### Example Endpoint

**GET `/v1/system/shutdown`**

- **Description**: Initiates a shutdown of the Raspberry Pi.
- **Response**:
  - **200 OK**: If the shutdown is initiated successfully.
  - **500 Internal Server Error**: If an error occurs while processing the request.

## Notes

- Consider implementing more robust logging and monitoring for the API to track usage and errors.
- Future versions of the API may include additional features such as user authentication, more granular control over camera settings, and enhanced error reporting.
- The API should be designed to be scalable and can be easily integrated with other systems and services.