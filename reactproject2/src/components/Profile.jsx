import React, { Component } from 'react'
import jwt_decode from 'jwt-decode'
import  Sidebar  from './sidebar'
class Profile extends Component {
  constructor() {
    super()
    this.state = {
      username: '',
      email: '',
      errors: {}
    }
  }

  componentDidMount() {
    const token = localStorage.usertoken
    const decoded = jwt_decode(token)
    this.setState({
      username: decoded.identity.username,
      email: decoded.identity.email
    })
  }

  render() {
    return (
      <div className="container">
        {/* <sidebar width={300} height={"100vh"}>
          <h2>Nav Item</h2>
          <h2>Nav Item</h2>
          <h2>Nav Item</h2>
          <h2>Nav Item</h2>
          <h2>Nav Item</h2>
        </sidebar> */}
        {/* <Sidebar pageWrapId={'page-wrap'} outerContainerId={'outer-container'} /> */}
        <div className="jumbotron mt-5">
          <div className="col-sm-8 mx-auto">
            <h1 className="text-body">PROFILE</h1>
          </div>
          <table className="table col-md-6 mx-auto">
            <tbody className="text-body">
              <tr>
                <td>Username</td>
                <td>{this.state.username}</td>
              </tr>
              <tr>
                <td>Email</td>
                <td>{this.state.email}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    )
  }
}

export default Profile
