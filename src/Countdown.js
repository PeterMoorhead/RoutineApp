import React, {ReactDOM} from 'react';


class Countdown extends React.Component {
    constructor(props) {
      super(props);
      this.state = { time: {}, seconds: 0 };
      this.timer = 0;
      this.startTimer = this.startTimer.bind(this);
      this.countDown = this.countDown.bind(this);
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
      console.log("time here: ", this.props.time);
      let timeLeftVar = this.secondsToTime(this.props.time.time);
      this.setState({ time: timeLeftVar, seconds: this.props.time.time });
      this.startTimer();
    }

    componentDidUpdate(prevProps) {
      if (this.props.time.time != prevProps.time.time) {
        let timeLeftVar = this.secondsToTime(this.props.time.time);
        this.setState({ time: timeLeftVar, seconds: this.props.time.time });
        this.startTimer();
      }
    }
  
    startTimer() {
      if (this.timer == 0 && this.state.seconds > 0) {
        this.timer = setInterval(this.countDown, 1000);
      }
    }
  
    countDown() {
      // Remove one second, set state so a re-render happens.
      let seconds = this.state.seconds - 1;
      this.setState({
        time: this.secondsToTime(seconds),
        seconds: seconds,
      });
      
      // Check if we're at zero.
      if (seconds == 0) { 
        clearInterval(this.timer);
      }
    }
  
    render() {
      this.startTimer();
      return(
        <div>
          <p>{this.props.time.task.task}</p>
          <button onClick={this.startTimer}>Start</button>
          <button onClick={this.startTimer}>Pause</button>
          m: {this.state.time.m} s: {this.state.time.s}
        </div>
      );
    }
  }
  
export default Countdown