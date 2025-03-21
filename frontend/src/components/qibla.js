import { Coordinates, CalculationMethod, PrayerTimes, SunnahTimes } from 'adhan';
import Compass from './Compass';

window.addEventListener("DOMContentLoaded", (event) => {

        const compassCircle = document.querySelector(".compass-circle");

        let latitude;
        let longitude;
        let compass;
        let inited = false;
        let orientation = null;
        let countDownInterval;
        let secondsLeftms;
        let endTime;
        let countDownTime;
        let userLocation;
        let directionAngle;
        const countDown = document.querySelector('#countdown');
        let timeMethod = "Tehran"
        const isIOS =
                navigator.userAgent.match(/(iPod|iPhone|iPad)/) &&
                navigator.userAgent.match(/AppleWebKit/);
        //TODO:

        let calculationMethod = localStorage.getItem('calculation-method') ?? 'MuslimWorldLeague';

        document.querySelector('#calculation-method').value = calculationMethod;

        const qiblaPoint = {
                lat: 21.422487,
                lng: 39.826206,
        };


        //sahre location

        document.getElementById('share_location').addEventListener('click', async function () {

                shareQibla();

        });

        function setCookie(name, value) {
                const expires = new Date();
                expires.setTime(expires.getTime() + (1 * 24 * 60 * 60 * 1000));
                const expiresString = "expires=" + expires.toUTCString();

                document.cookie = name + "=" + value + ";" + expiresString + ";path=/";
        }

        //change prayer time method

        document.querySelector('#calculation-method').addEventListener('change', (e) => {

                timeMethod = e.target.value;

                localStorage.setItem('calculation-method', timeMethod);

                if (latitude && longitude) {

                        setPrayerTime(timeMethod);
                }

        });

        //Change Lang

        document.querySelector(".language").addEventListener("click", function () {

                document.querySelector(".lang").classList.toggle("active");
        })

        //Change theme

        document.querySelector(".change-theme").addEventListener("click", function () {

                document.querySelector(".colors").classList.toggle("active");
        });

        //Change Color

        document.querySelectorAll(".color").forEach(el => {

                el.addEventListener("click", function () {

                        document.querySelector(".color.active").classList.remove("active");

                        el.classList.add("active");

                        if (el.classList.contains("active")) {

                                var rotateVal = el.getAttribute("data-id");
                                var color = el.style.backgroundColor;

                                document.querySelector(".compass").style.filter =
                                        `hue-rotate(${rotateVal}deg)`;

                                document.documentElement.style.setProperty("--main-color", color);

                                document.querySelector(".info-text").style.filter =
                                        `hue-rotate(${rotateVal}deg)`;

                                document.querySelector(".prayer-time .active .head").style.filter =
                                        `hue-rotate(${rotateVal}deg)`;


                                document.querySelector(".prayer-time .active i").style.filter =
                                        `hue-rotate(${rotateVal}deg)`;

                                document.querySelector(".prayer-time .active span:last-of-type").style.filter =
                                        `hue-rotate(${rotateVal}deg)`;
                        }

                })

        });

        document.querySelector(".toggle")?.addEventListener("click", function (e) {

                e.preventDefault();

                this.classList.toggle("toggle-on");

                document.querySelector(".info-text").classList.toggle('active');

                if (this.classList.contains("toggle-on")) {

                        initPremissions();

                        if (!isIOS) {

                                window.addEventListener("deviceorientationabsolute", updateRotationAndQibla);

                        } else if (isIOS) {

                                window.addEventListener("deviceorientation", updateRotationAndQibla, true);
                        }
                }
        })

        async function initPremissions() {

                if (typeof window.DeviceOrientationEvent.requestPermission === "function") {

                        const permission = await window.DeviceOrientationEvent.requestPermission();

                        if (permission == "granted") {

                                orientation = true;

                                await initCompass();

                        } else {

                                orientation = false;

                                await initCompass();

                        }
                } else if (window.DeviceOrientationEvent) {

                        orientation = true;

                        await initCompass();

                } else {

                        orientation = false;

                        await initCompass();

                }

                compass = new Compass();

                const location = await new Promise((resolve, reject) => {
                        navigator.geolocation.getCurrentPosition((position) => {
                                if (position) {
                                        resolve(position);
                                } else {
                                        reject(null);
                                }
                        });
                });

                if (location) {

                        latitude = location.coords.latitude;
                        longitude = location.coords.longitude;

                        if (!inited) {
                                showPosition();
                                inited = true;
                        }
                } else {
                        showError();
                }
        }

        function showError(error) {
                switch (error.code) {
                        case error.PERMISSION_DENIED:
                                alert("{{ lang[$currentLang ?? 'en']['text']['user_denied'] }}");
                                return;
                                break;
                        case error.POSITION_UNAVAILABLE:
                                alert(
                                        "{{ lang[$currentLang ?? 'en']['text']['information_unavailable'] }}"
                                );
                                return;
                                break;
                        case error.TIMEOUT:
                                alert("{{ lang[$currentLang ?? 'en']['text']['timed_out'] }}");
                                return;
                                break;
                }
        }

        function showPosition() {

                if (inited) {
                        initCompass();
                        return;
                }

                const qiblaAngle = calcQiblaDirection(latitude, longitude);
                const qiblaDirection = getCardinalDirection(qiblaAngle);

                document.querySelector(".latitude span").innerText = latitude;
                document.querySelector(".longitude span").innerText = longitude;
                directionAngle = `${qiblaDirection} ${qiblaAngle}`;
                document.querySelector(".deg span").innerText = `${qiblaDirection} ${qiblaAngle}`;

                initCompass();

                setPrayerTime();
                distanceCoordinates();
                getCurrentTimeInSaudiArabia();

                setCookie("longitude", longitude);
                setCookie("latitude", latitude);
                setCookie("userLocation", userLocation);
                setCookie("directionAngle", directionAngle);

                GetAltitude();
        }

        function calcQiblaDirection(userLatitude, userLongitude) {
                const qiblaPoint = {
                        lat: 21.422487,
                        lng: 39.826206,
                };

                const phi1 = (userLatitude * Math.PI) / 180;
                const lambda1 = (userLongitude * Math.PI) / 180;
                const phi2 = (qiblaPoint.lat * Math.PI) / 180;
                const lambda2 = (qiblaPoint.lng * Math.PI) / 180;

                const deltaLambda = lambda2 - lambda1;
                const y = Math.sin(deltaLambda) * Math.cos(phi2);
                const x =
                        Math.cos(phi1) * Math.sin(phi2) -
                        Math.sin(phi1) * Math.cos(phi2) * Math.cos(deltaLambda);

                let psi = (Math.atan2(y, x) * 180) / Math.PI;

                if (psi < 0) {
                        psi += 360;
                }

                return Math.round(psi);
        }

        function getCardinalDirection(degree) {
                const directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"];

                const index = Math.round(degree / 45) % 8;

                return directions[index >= 0 ? index : index + 8];
        }

        async function initCompass() {

                if (!latitude || !longitude || compass == undefined) {
                        return;
                }

                if (orientation && !inited) {
                        if (compass && typeof compass.allowOrientationPermissions === 'function') {
                                await compass.allowOrientationPermissions();
                        }
                }

                await compass.init(updateRotationAndQibla);
        }

        function updateRotationAndQibla(event) {
                if (!compass) return;

                let deg = 0;

                const currentPosition = {
                        lat: latitude,
                        lng: longitude,
                };

                const angleToKaaba = compass.getBearingToDestination(currentPosition, {
                        lat: qiblaPoint.lat,
                        lng: qiblaPoint.lng,
                });

                deg = smoothDegreeTransition(deg, Math.round(angleToKaaba));

                document.querySelector(".compass").style.transform = `rotate(${deg}deg)`;
        }

        function smoothDegreeTransition(oldDeg, newDeg) {

                let diff = newDeg - oldDeg;

                while (diff < -180) {
                        diff += 360;
                }

                while (diff > 180) {
                        diff -= 360;
                }

                return oldDeg + diff;
        }

        function setPrayerTime(calculationMethod = 'MuslimWorldLeague') {

                // const coordinates = new Coordinates(35.3391979, 51.6291533);
                const coordinates = new Coordinates(latitude, longitude);
                const params = CalculationMethod[calculationMethod]();
                const date = new Date();
                const prayerTimes = new PrayerTimes(coordinates, date, params);
                const fajrTime = formatTime(prayerTimes.fajr);
                const ishaTime = formatTime(prayerTimes.isha);
                const maghribTime = formatTime(prayerTimes.maghrib);
                const dhuhrTime = formatTime(prayerTimes.dhuhr);
                const asrTime = formatTime(prayerTimes.asr);

                document.querySelector('.dawn span:last-of-type').innerText = fajrTime;
                document.querySelector('.noon span:last-of-type').innerText = dhuhrTime;
                document.querySelector('.afternoon span:last-of-type').innerText = asrTime;
                document.querySelector('.maghrib span:last-of-type').innerText = maghribTime;
                document.querySelector('.isha span:last-of-type').innerText = ishaTime;

                const prayerTimesArray = {
                        fajr: fajrTime,
                        isha: ishaTime,
                        maghrib: maghribTime,
                        dhuhr: dhuhrTime,
                        asr: asrTime
                };

                let nextPrayer = findNextPrayerTime(prayerTimesArray);
                let nextDayFlag = false;

                if (nextPrayer == null) {

                        nextPrayer = "fajr";

                        nextDayFlag = true;
                }

                document.querySelector(`#time-${nextPrayer}`)?.classList.add("active");

                let currentTime = getCurrentTime();


                let currentDate = new Date()
                currentDate = currentDate.toISOString().split('T')[0];
                currentDate = currentDate.replace("/-/g", "/");

                let currentDateTime = new Date(`${currentDate} ${currentTime}`);
                let nextDateTime = new Date(`${currentDate} ${prayerTimesArray[nextPrayer]}`)


                if (nextDayFlag) {

                        nextPrayer = "fajr";

                        document.querySelector(`#time-fajr`)?.classList.add("active");

                        let nextDay = new Date()
                        nextDay.setDate(nextDay.getDate() + 1);
                        getNextDayPrayerTime(nextDay);
                        nextDay = nextDay.toISOString().split('T')[0];
                        nextDay = nextDay.replace("/-/g", "/");

                        nextDateTime = new Date(`${nextDay} ${prayerTimesArray["fajr"]}`);
                }


                let difference = nextDateTime.getTime() - currentDateTime.getTime();
                let resultInMinutes = Math.floor((difference - 0 * 60000) / 60000);

                countDownTime = resultInMinutes;
                countDownTime = countDownTime * 60000;

                const now = Date.now();
                endTime = now + countDownTime;

                document.querySelector(".next-time").classList.add("active");

                setCountDown(endTime);

                countDownInterval = setInterval(() => {
                        setCountDown(endTime);
                }, 1000);
        }

        function setCountDown(endTime) {

                secondsLeftms = endTime - Date.now();
                const secondsLeft = Math.round(secondsLeftms / 1000);

                let hours = Math.floor(secondsLeft / 3600);
                let minutes = Math.floor(secondsLeft / 60) - (hours * 60);
                let seconds = secondsLeft % 60;

                if (hours < 10) {
                        hours = `0${hours}`;
                }
                if (minutes < 10) {
                        minutes = `0${minutes}`;
                }
                if (seconds < 10) {
                        seconds = `0${seconds}`;
                }

                if (secondsLeft < 0) {
                        resetCountDown();
                        return;
                }

                countDown.innerHTML = `${hours} : ${minutes} : ${seconds}`;

        }

        function getNextDayPrayerTime(day) {
                const coordinates = new Coordinates(latitude, longitude);
                const params = CalculationMethod[calculationMethod]();
                const prayerTimes = new PrayerTimes(coordinates, day, params);
                const fajrTime = formatTime(prayerTimes.fajr);

                document.querySelector('.dawn span:last-of-type').innerText = fajrTime;
        }

        function resetCountDown() {

                clearInterval(countDownInterval);
                countDown.innerHTML = '00 : 00 : 00';
        }

        function changeTimezone(date, ianatz) {


                var invdate = new Date(date.toLocaleString('en-US', {
                        timeZone: ianatz
                }));


                var diff = date.getTime() - invdate.getTime();

                return new Date(date.getTime() - diff);
        }

        function getTimeZoneFromCity(cityName) {
                // Extract the city name from the user's input
                const city = cityName.split('/')[1].trim(); // Assuming the format is "Country / City"

                // Loop through the array of IANA time zones
                for (let i = 0; i < aryIanaTimeZones.length; i++) {
                        // Check if the city name is present in the IANA time zone string
                        if (aryIanaTimeZones[i].toLowerCase().includes(city.toLowerCase())) {
                                // Return the matching time zone
                                return aryIanaTimeZones[i];
                        }
                }

                // If no matching time zone is found, return null
                return null;
        }
        
        function getCurrentTime() {
                
                const now = new Date();
                const hours = now.getHours().toString().padStart(2, '0');
                const minutes = now.getMinutes().toString().padStart(2, '0');

                return `${hours}:${minutes}`;
        }

        function timeToMinutes(time) {
                const [hours, minutes] = time.split(':').map(Number);
                return hours * 60 + minutes;
        }


        function formatTime(time) {

                return time.toLocaleTimeString('en-US', { hour12: false });
        }

        function degreesToRadians(degrees) {

                return degrees * Math.PI / 180;
        }

        function distanceCoordinates() {
                const earthRadiusKm = 6371;
                const earthRadiusMiles = 3958.8;
                const averageSpeed = 60;

                const dLat = degreesToRadians(qiblaPoint.lat - latitude);
                const dLon = degreesToRadians(qiblaPoint.lng - longitude);

                const a =
                        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                        Math.cos(degreesToRadians(latitude)) * Math.cos(degreesToRadians(qiblaPoint.lat)) *
                        Math.sin(dLon / 2) * Math.sin(dLon / 2);

                const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

                const distanceKm = earthRadiusKm * c;
                const distanceMiles = earthRadiusMiles * c;

                const distanceKmRounded = Math.round(distanceKm);
                const distanceMilesRounded = Math.round(distanceMiles);

                document.querySelector(".distance span:last-of-type").innerText = `${distanceKmRounded.toLocaleString()} km (${distanceMilesRounded.toLocaleString()} miles)`;
        }

        function getCurrentTimeInSaudiArabia() {

                const currentDate = new Date();

                currentDate.setTime(currentDate.getTime());

                const formattedTime = currentDate.toLocaleTimeString('en-US');

                document.querySelector(".current-time span:last-of-type").innerText = formattedTime;
        }

        function timeToMinutes(time) {
                const [hours, minutes] = time.split(':').map(Number);
                return hours * 60 + minutes;
        }

        function findNextPrayerTime(prayerTimes) {
                const currentTime = getCurrentTime();                

                const times = Object.keys(prayerTimes);
                let minDifference = Infinity;
                let nextPrayer = null;

                times.forEach(prayer => {
                        const timeDifference = timeToMinutes(prayerTimes[prayer]) - timeToMinutes(currentTime);

                        if (timeDifference > 0 && timeDifference < minDifference) {
                                minDifference = timeDifference;
                                nextPrayer = prayer;
                        }
                });

                return nextPrayer;
        }


        document.querySelectorAll('.title_box h2').forEach(element => {

                element.addEventListener("click", function () {

                        element.parentElement.classList.toggle("active");
                })
        });
});