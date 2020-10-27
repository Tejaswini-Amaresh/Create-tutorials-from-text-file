import React, { Component } from 'react'

class Assessment extends Component {
    constructor(props) {
        super(props);
    
         this.state = {
           questions: {}
        };
    
        this.gen_questions = this.gen_questions.bind(this);
      }
      componentDidMount() {
        this.gen_questions();
     }
    
      gen_questions(){
        // ev.preventDefault();
        fetch('http://localhost:5000/assessments', {
      method: 'POST',
      body:JSON.stringify({'data':this.props.location.data}),
      headers: new Headers({
        "content-type": "application/json"
      }),
    }).then((response) => {
      response.json().then((body) => {
        this.setState({ questions: body.data});
        console.log(this.state.questions);
        // document.getElementById("text").innerHTML=body.text;
        // document.getElementById("summary").innerHTML=body.summary;
        // document.getElementsByClassName("heading")[0].style.visibility="visible";
        // document.getElementsByClassName("container1")[0].style.visibility="visible";
        // document.getElementsByClassName("heading")[0].style.display="flex";
        // document.getElementsByClassName("container1")[0].style.display="flex";
      });
    });
  }
  render() {
    //   this.gen_questions()
    return (
    //   <div className="container" onLoad={this.gen_questions}>
    //     <ul>
    //   {this.state.questions.map((value, index) => {
    //     return <li key={index}>{value}</li>
    //   })}
    // </ul>
    //     <div className="jumbotron mt-5">
    //       <div className="col-sm-8 mx-auto">
    //         <h1 className="text-body">{this.props.location.data}</h1>
    //       </div>
    //     </div>
    //   </div>
    <form>
    <div>
      {
        Object.keys(this.state.questions).map((key, index) => ( 
            <div className="jumbotron mt-5" key={index}>
           <div className="col-sm-8 mx-auto">
          <h5 className="text-body">  {this.state.questions[key][1]}</h5> 
          <textarea defaultValue="Type your answer here"></textarea>
          </div>
          </div>
        ))
      }
    </div>
    </form>
    )
  }
}

export default Assessment