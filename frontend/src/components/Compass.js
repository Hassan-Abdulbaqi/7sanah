class Compass {
    /**
     * The compass class is a utility for creating a javascript compass
     * with no external dependencies. You can create a compass that
     * points north from your location or points towards a specified
     * latitude and longitude coordinate. Regardless of where you turn
     * the compass will point towards the specified direction.
     *
     * @class
     */
    constructor() {
        this.heading = 0;
        this.deviceAngleDelta = 0;
        this.position = null;

        this.geolocationID = null;
        this.permissionGranted = false;
        this.isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
    }

    /**
     * initialized the compass - returns a promise or can invoke a callback
     * @param {callback} callback - callback to be called after the .start() function is done
     */
    init(callback = undefined) {
        if (callback) {
            this.callCallback(this.start(), callback);
        } else {
            return this.start();
        }
    }

    /**
     * Initializes the device orientation and watches the user position by default
     * @async
     * @function start
     *
     */
    async start() {
        try {
            await this.watchPosition();
            return true;
        } catch (err) {
            alert(err);
        }
    }

    /**
     * Asks the user to allow permissions to get orientation
     *
     * @async
     * @name allowOrientationPermissions
     */
    async allowOrientationPermissions() {
        if (typeof window.DeviceOrientationEvent.requestPermission === "function") {
            const permission = await window.DeviceOrientationEvent.requestPermission();

            if (permission == "granted") {
                this.permissionGranted = true;
                this.handleOrientationEvent();
                return true;
            } else {
                throw new Error("no device orientation permissions!");
            }

        } else {
            if (window.DeviceOrientationEvent) {
                this.permissionGranted = true;
                this.handleOrientationEvent();
                return true;
            } else {
                throw new Error("no device orientation support!");
            }
        }
    }

    async handleOrientationEvent() {
        if (this.isIOS) {
            window.addEventListener(
                "deviceorientation",
                this.deviceOrientationHandler.bind(this),
                true
            );
        } else {
            window.addEventListener(
                "deviceorientationabsolute",
                this.deviceOrientationHandler.bind(this),
                true
            );
        }
    }

    /**
     * This is where my nose points - and seeing as my nose
     * is attached to my head, this is where my head
     * (and thus my machine) is pointing relative to North.
     * NOTE: requires that this.position is set
     *
     * @function getHeading
     */
    getHeading(
        origin = {
            lat: this.position.coords.latitude,
            lng: this.position.coords.longitude,
        },
        north = { lat: 90, lng: this.position.coords.longitude }
    ) {
        this.heading = 360 - this.getBearingToNorth(origin, north);
        return this.heading;
    }

    /**
     * This is the angle between the location of an object,
     * machine or destination and my heading.
     *
     * @param {Object} origin - {lat, lng}
     * @param {Object} destination - {lat, lng}
     */
    getBearing(origin, destination) {
        return (
            this.calculateAngle(
                origin.lat,
                origin.lng,
                destination.lat,
                destination.lng
            ) *
            (180 / Math.PI)
        );
    }

    /**
     * get the angle between your heading and north
     * the default is true north vs. magnetic north
     *
     * @function
     * @param {object} origin - {lat, lng}
     * @param {object} north - {lat, lng}
     */
    getBearingToNorth(
        origin = {
            lat: this.position.coords.latitude,
            lng: this.position.coords.longitude,
        },
        north = { lat: 90, lng: this.position.coords.longitude }
    ) {
        return this.getBearingToDestination(origin, north);
    }

    /**
     * Get the bearings towards the destination
     *
     * @param {object} origin - {lat, lng}
     * @param {object} destination - {lat, lng}
     */
    getBearingToDestination(
        origin = {
            lat: this.position.coords.latitude,
            lng: this.position.coords.longitude,
        },
        destination
    ) {
        const angleToDestination = this.getBearing(origin, destination);
        return this.deviceAngleDelta + angleToDestination;
    }

    /**
     * Handles changes created by the device orientation changes
     * assumes that the phone is in a portrait mode, with the display up
     * towards the sky as if you were holding an actual compass
     *
     * @callback
     * @param {object} evt - the event object of the device orientation
     */
    deviceOrientationHandler(evt) {
        if (evt.webkitCompassHeading) {
            //iphone
            this.deviceAngleDelta = 360 - evt.webkitCompassHeading;
        } else if (evt.alpha) {
            //android
            this.deviceAngleDelta = 360 - Math.abs(evt.alpha - 360);
        } else {
           
        }
        this.deviceAngleDelta = Math.round(this.deviceAngleDelta);
    }

    /**
     * get the position of the user
     *
     * @async
     * @function
     */
    getPosition() {
        return new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition((position) => {
                if (position) {
                    resolve(position);
                } else {
                    reject("no position found");
                }
            });
        });
    }

    /**
     * watches the geolocation of the user
     *
     * @async
     * @function
     */
    watchPosition() {
        return new Promise((resolve, reject) => {
            this.geolocationID = navigator.geolocation.watchPosition((position) => {
                if (position) {
                    this.position = position;
                    resolve(position);
                } else {
                    reject("no position found");
                }
            });
        });
    }

    /**
     * Stops watching the user location
     *
     * @function
     */
    stopTracking() {
        navigator.geolocation.clearWatch(this.geolocationID);
    }

    /**
     * Calculates the angle given a latitude and longitude position
     *
     * @function
     * @param {number} userLat - user latitude
     * @param {number} userLon - user longitude
     * @param {number} desiredLat - desired latitude
     * @param {number} desiredLon - desired longitude
     */
    calculateAngle(userLat, userLon, desiredLat, desiredLon) {
        return Math.atan2(desiredLon - userLon, desiredLat - userLat);
    }

    /**
     * Helper function that allows calling a callback from an promise function
     *
     * @param {promise} promise
     * @param {callback} callback
     */
    callCallback(promise, callback) {
        if (callback) {
            promise
                .then((result) => {
                    callback(undefined, result);
                    return result;
                })
                .catch((error) => {
                    callback(error);
                    return error;
                });
        }
        return promise;
    }
}

export default Compass; 