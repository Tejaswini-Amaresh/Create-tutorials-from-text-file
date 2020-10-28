import React, { Component } from 'react'

class Assessment extends Component {
    constructor(props) {
        super(props);
    
         this.state = {
           boolean_question: {},
           mcq:{}
        };
    
        this.gen_questions = this.gen_questions.bind(this);
        this.onSubmit=this.onSubmit.bind(this);
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
        this.setState({ boolean_question: body.bool, mcq:body.mcq});
        console.log(this.state);
        // document.getElementById("text").innerHTML=body.text;
        // document.getElementById("summary").innerHTML=body.summary;
        // document.getElementsByClassName("heading")[0].style.visibility="visible";
        // document.getElementsByClassName("container1")[0].style.visibility="visible";
        // document.getElementsByClassName("heading")[0].style.display="flex";
        // document.getElementsByClassName("container1")[0].style.display="flex";
      });
    });
  }
  onSubmit(e) {
    e.preventDefault()
    // var formElements = 
    console.log(this.state.questions.length);
    for(var i=0;i<Object.keys(this.state.questions).length;i++){
      this.state.questions[i].push(document.forms['qa'].elements[i.toString()].value);
    }

    console.log(this.state.questions);
    
  }

  render() {
    //   this.gen_questions()
    return (
    // <form noValidate onSubmit={this.onSubmit}>
    <form noValidate onSubmit={this.onSubmit} name="qa">
    <div>
      {
        Object.keys(this.state.mcq).map((key, index) => ( 
            <div className="jumbotron mt-5" key={index}>
           <div className="col-sm-8 mx-auto">
          <h5 className="text-body">{index+1}) {this.state.mcq[key]["question_statement"]}</h5> 

          {
          this.state.mcq[key]["options"].map((option,index1) => (
            <div style={{color: 'black', textAlign: 'left'}}>
              <input type="radio" name="question" id={index1} value={index1}/><label for={index1}>  {option}</label>
            </div>)
          )}
          </div>
          </div>
        ))
      }
    </div>
    <input type="submit"/>
    </form>
    )
  }
}

export default Assessment