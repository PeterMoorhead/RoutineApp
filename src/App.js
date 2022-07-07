import React from 'react';
import logo from './logo.svg';
import './App.css';
import ApiService from './apiService';
import Countdown from './Countdown';

class App extends React.Component {
  
  constructor(props) {
    super(props);
    this.state = {
      paused: false,
      time: 0,
      task: ""
    }
    this.timer = 0;
    this.handleFinishedTask = this.handleFinishedTask.bind(this);
    this.pauseCurrentTask = this.pauseCurrentTask.bind(this);
  }

  componentDidMount() {
    this.handleFinishedTask();
  }

  componentDidUpdate() {
    clearInterval(this.timer);
    this.timer = setInterval(this.handleFinishedTask, 30000);
  }

  handleFinishedTask() {
    fetch('http://localhost:5000/getRoutine').then(res => res.json()).then(data => {
      console.log(data);
      console.log(Object.values(data.currentTask)[0]);
      console.log(Object.keys(data.currentTask)[0]);
      this.setState({paused: data.paused, time: Object.values(data.currentTask)[0], task: Object.keys(data.currentTask)[0].toString()});
    })
  }

  pauseCurrentTask() {
    fetch('http://localhost:5000/pause').then(res => res.json()).then(data => {
      this.setState({paused: data.paused});
    })
  }  
  
  startCurrentTask() {
    fetch('http://localhost:5000/start').then(res => res.json()).then(data => {
      console.log("retun from start: ", data);
      this.setState({paused: data.paused});
    })
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h3>{this.state.task}</h3>
          <Countdown time={this.state.time} task={this.state.task} handleChange={this.handleFinishedTask} pause={this.pauseCurrentTask} start={this.startCurrentTask} paused={this.state.paused}/>
        </header>
      </div>
    );
  }
}

export default App;
