Based on [OpenScan3](https://github.com/OpenScan-org/OpenScan3)

## 1. Core Infrastructure & Setup

- [ ] Update initial setup procedure
- [x] Basic FastAPI application structure setup (already done in app-main.py)
- [ ] Configure settings for different hardware setups (greenshield, blackshield, grblHAL)
- [ ] Set up error handling and logging system
- [ ] Implement Network security
- [ ] Use virtual environment
- [ ] Integrate ramdisk for faster temporary file handling

### 1.1. Network & Connectivity
- [ ] Add hotspot mode
- [ ] Add wifi configuration & testing
- [ ] Add test for internet connectivity

## 2. Hardware Control Components

### 2.1. Camera System 

- [ ] Review and update camera controllers (gphoto2, v4l2, picamera2)
- [ ] Implement unified camera interface
- [ ] Implement camera settings management
- [ ] Integrate Focus control system:
  - [ ] Integrate software controlled focus
  - [ ] Add mechanic focus through third motor

### 2.2. Motor Control System

- [ ] Migrate motor controllers from old system (directly through GPIO)
- [ ] Add Motor controller through GRBLhal
- [ ] Integrate optional endstops
- [ ] Implement motor movement coordination
- [ ] Add tests for users

### 2.3. Light Control system

- [ ] Migrate Light controller (directly through GPIO)
- [ ] Add Light controller through GRBLhal
- [ ] Add tests for users

### 2.4. Fan Control System
- [ ] Add fan controller (directly through GPIO)
- [ ] Add Fan controller through GRBLhal
- [ ] Add Temperature dependent fan control

### 2.5. Other Peripherals ?

## 3. Scanning Logic

### 3.1 Smart Pre-Scan systems (nice to have/optional)

- [ ] Add auto-exposure detection based on histogram
- [ ] Add auto-crop detection routine
- [ ] Add auto-depth detection
- [ ] Add Evaluation of object preparation (feature detection)

### 3.2. Core Scanning System

- [ ] Add scan templates/presets
- [ ] Migrate scanning process controller
- [ ] Implement proper scan state management
  - [ ] Add scan progress tracking
  - [ ] Add resume from failure point
  - [ ] Implement pause/resume functionality

### 3.3. Path Generation

- [ ] Migrate different scanning patterns (Grid, Fibonacci, Spiral, Archimedes)
- [ ] Implement path optimization
- [ ] Add path visualization support

### 4. Scan Project Handling

- [ ] Implement project creation and management
- [ ] Implement proper file structure for projects
- [ ] Add External drive for saving
- [ ] Add network drive for saving
- [ ] Add project metadata handling
- [ ] Add download project
- [ ] Add delete project
- [ ] Add delete all projects
- [ ] Add merge projects
- [ ] Add scan meta data (positions, focus, resolution, timestamps)

## 5. Processing Integration

### 5.1. OpenScan Cloud

- [ ] Migrate cloud upload functionality
- [ ] Implement secure authentication
- [ ] Add progress tracking for uploads
- [ ] Implement download functionality

### 5.2. create Project files for other programs
- [ ] Metashape
- [ ] Reality Capture
- [ ] 3DF Zephyr
- [ ] Meshroom

## 6. System Services

- [ ] Migrate system status monitoring
- [ ] Implement proper shutdown/reboot handlers
- [ ] Add system health checks
- [ ] Add system statistics
- [ ] Add Diskspace monitoring
- [ ] Add Diskspace warnings
- [ ] Implement update service
- [ ] Implement update versioning
- [ ] Add Change Log
- [ ] Add Server message service
- [ ] Add Samba client
- [ ] Add SSH on/off


## 7. Testing ??
- [ ] Set up unit testing infrastructure
- [ ] Add integration tests
- [ ] Implement hardware simulation for testing
- [ ] Add CI/CD pipeline


## 8. Documentation

- [ ] API documentation
- [ ] System architecture documentation
- [ ] Hardware setup documentation
- [ ] User guide


