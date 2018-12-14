function controller() {
    return {
        moarSpeed: function () {
            if (this.throttle < this.maxThrottle)
                this.throttle += 1;
        },
        goSlower: function () {
            if (this.throttle > this.minThrottle)
                this.throttle -= 1;
        },
        goLeft: function () {
            if (this.rudder >= this.minRudder)
                this.rudder -= 1;
        },
        goRight: function () {
            if (this.rudder <= this.maxRudder)
                this.rudder += 1;
        },
        trimLeft: function () {
            if (this.rudderTrim > this.minRudderTrim)
                this.rudderTrim -= 1;
        },
        trimRight: function () {
            if (this.rudderTrim < this.maxRudderTrim)
                this.rudderTrim += 1;
        },
        moarMultiplier: function () {
            if (this.rudder <= this.maxMultiplier)
                this.throttleMultiply += this.throttleMultiply;
        },
        lessMultiplier: function () {
            if (this.rudder >= this.minMultiplier)
                this.throttleMultiply -= this.throttleMultiply;
        },
        hardStop: function () {
            this.throttle = this.minThrottle;
        },
        fullSpeedAheadCaptain: function () {
            this.throttle = this.maxThrottle;
        },
        returnRudder: function () {
            if (this.rudder < 0) {
                this.rudder += 1;
                return true;
            }else
            if (this.rudder > 0) {
                this.rudder -= 1;
                return true;
            }
            return false;
        },
        forward: function () {
            this.direction = 'Forward';
        },
        reverse: function () {
            this.direction = 'Reverse';
        },
        getData: function(){
            return {
                throttle : this.throttle,
                rudder: this.rudder,
                rudderTrim: this.rudderTrim,
                throttleMultiply: this.throttleMultiply,
                direction: this.direction,
                maxThrottle: this.maxThrottle,
                minThrottle: this.minThrottle,
                maxRudder: this.maxRudder,
                minRudder: this.minRudder,
                maxMultiplier: this.maxMultiplier,
                minMultiplier: this.minMultiplier,
                maxRudderTrim: this.maxRudderTrim,
                minRudderTrim: this.minRudderTrim
            };
        },

        throttle: 0,
        rudder: 0,
        rudderTrim: 0,
        throttleMultiply: 1,
        direction: 'Forward',
        maxThrottle: 10,
        minThrottle: 0,
        maxRudder: 10,
        minRudder: -10,
        maxMultiplier: 2,
        minMultiplier: 1,
        maxRudderTrim: 10,
        minRudderTrim: -10
    }
}