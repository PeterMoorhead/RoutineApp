import './App.css';

const ApiService = {
  pause: function(e) {
    e.preventDefault();
      fetch('http://localhost:5000/pause');
  },
  start: function(e) {
    e.preventDefault();
    fetch('http://localhost:5000/getRoutine');
  }
};

export default ApiService;
