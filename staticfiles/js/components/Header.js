class Header {
    constructor(counter) {
        this.counter = counter;
        this.api = api;
        this.counterNum = this.counter.textContent;
        this.plusCounter = this.plusCounter.bind(this);
        this.minusCounter = this.minusCounter.bind(this);
    }
    adjustCounterVisibility() {
        if (this.counterNum === 0) {
            this.counter.style.visibility = "hidden";
        } else {
            this.counter.style.visibility = "visible";
        }
    }
    plusCounter() {
        this.counterNum = ++this.counterNum;
        this.counter.textContent = this.counterNum;
        this.adjustCounterVisibility();
    }
    minusCounter() {
        this.counterNum = --this.counterNum;
        this.counter.textContent = this.counterNum;
        this.adjustCounterVisibility();
    }
}
