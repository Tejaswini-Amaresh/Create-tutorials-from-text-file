import React from 'react';
import Tutorial from './components/Tutorial';
import './app.css';

import { BrowserRouter as Router, Route } from 'react-router-dom'

import Navbar from './components/Navbar'
import Landing from './components/Landing'
import Login from './components/Login'
import Register from './components/Register'
import Profile from './components/Profile'
import Assessment from './components/Assessment'
import logo from './hi.png';
const App = () => (
  <div>
    <br></br>
    <img src={logo} align="right" height="170px" width="200px"/>
    <h1 className="heading1">Tutorial Generation</h1>
    <br></br><hr></hr>
    <Router>
        <div className="App">
          <Navbar />
          <Route exact path="/" component={Landing} />
          <div className="container">
            <Route exact path="/register" component={Register} />
            <Route exact path="/tutorial_gen" component={Tutorial} />
            <Route exact path="/login" component={Login} />
            <Route exact path="/profile" component={Profile} />
            <Route exact path="/assessments" component={Assessment} />
          </div>
        </div>
      </Router>
  </div>
);

export default App;