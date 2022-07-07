import React from 'react';


class Countdown extends React.Component {
    constructor(props) {
      super(props);
      this.state = { time: {}, seconds: 0, started: false };
      this.timer = 0;
      this.startTimer = this.startTimer.bind(this);
      this.countDown = this.countDown.bind(this);
      this.pauseTime = this.pauseTime.bind(this);
    }
  
    secondsToTime(secs){
      let hours = Math.floor(secs / (60 * 60));
  
      let divisor_for_minutes = secs % (60 * 60);
      let minutes = Math.floor(divisor_for_minutes / 60);
  
      let divisor_for_seconds = divisor_for_minutes % 60;
      let seconds = Math.ceil(divisor_for_seconds);
  
      let obj = {
        "h": hours,
        "m": minutes,
        "s": seconds
      };
      return obj;
    }
  
    componentDidMount() {
      let timeLeftVar = this.secondsToTime(this.props.time);
      this.setState({ time: timeLeftVar, seconds: this.props.time });
      this.startTimer();
    }

    componentDidUpdate(prevProps) {
      console.log("this.props.time: ", this.props.time)
      console.log("prevprops: ", prevProps.time)
      if (this.props.time != prevProps.time) {
        let timeLeftVar = this.secondsToTime(this.props.time);
        this.setState({ time: timeLeftVar, seconds: this.props.time, started: true });
        this.startTimer();
      }
    }
  
    startTimer() {
      if (this.timer == 0 && this.state.seconds > 0) {
        this.timer = setInterval(this.countDown, 1000);
      }
    }

    pauseTime() {
      clearInterval(this.timer);
      this.props.pause();
    }

    countDown() {
      // Remove one second, set state so a re-render happens.
      let seconds = this.state.seconds - 1;
      this.setState({
        time: this.secondsToTime(seconds),
        seconds: seconds,
        started: true
      });
      
      // Check if we're at zero.
      if (seconds == 0) { 
        clearInterval(this.timer);      
        // this.setState({
        //   started: false
        // });
        this.props.handleChange();
      }
    }
  
    render() {
      return(
        <div>
          {this.props.paused && <button onClick={() => {this.props.start()}}>Start</button>}
          {!this.props.paused && <button onClick={() => {this.pauseTime()}}>Pause</button>}
          m: {this.state.time.m} s: {this.state.time.s}
        </div>
      );
    }
  }
  
export default Countdown