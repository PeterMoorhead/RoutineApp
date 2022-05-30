import React from 'react';
import logo from './logo.svg';
import './App.css';
import ApiService from './apiService';
import Countdown from './Countdown';

class App extends React.Component {
  
  constructor(props) {
    super(props);
    this.state = {
      time: 0,
      task: {}
    }
    this.test = this.test.bind(this);
  }

  componentDidMount() {
    fetch('http://localhost:5000/getRoutine').then(res => res.json()).then(data => {
      console.log(data);
      this.setState({time: data.currentTask.time, task: data.currentTask});
    })
  }

  test() {
    fetch('http://localhost:5000/getRoutine').then(res => res.json()).then(data => {
      console.log(data);
      this.setState({time: data.currentTask.time + 1});
    })
  }

  // componentDidMount() {
  //   if (this.state != this.state){
  //     fetch('http://localhost:5000/getRoutine').then(res => res.json()).then(data => {
  //       console.log(data);
  //       this.setState({time: data.currentTask.time});
  //     })
  //   }
  // }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
          <p><Countdown time={this.state}/></p>
          <button onClick={(e) => {ApiService.pause(e)}}>Pause</button>
          <button onClick={(e) => {ApiService.start(e)}}>Start</button>
          <button onClick={this.test}>{this.state.time}</button>
        </header>
      </div>
    );
  }
}

export default App;
