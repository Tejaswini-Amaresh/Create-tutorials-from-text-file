import React from 'react';
import './app.css';

class Main extends React.Component {
  constructor(props) {
    super(props);

     this.state = {
       text1: '',
       summary1: '',
       mapping: {},
       ppt_path: '',
       fname: '',
    };

    this.handleUploadImage = this.handleUploadImage.bind(this);
    this.createPPT = this.createPPT.bind(this);
  }

  handleUploadImage(ev) {
    ev.preventDefault();

    const data = new FormData();
    data.append('Upload', this.uploadInput.files[0]);
    data.append('filename', this.fileName.value);

    fetch('http://localhost:5000/submit', {
      method: 'POST',
      body: data,
    }).then((response) => {
      response.json().then((body) => {
        this.setState({ text1: body.text,  summary1: body.summary, mapping:body.mapping, fname:body.fname });
        console.log(this.state);
        document.getElementById("text").innerHTML=body.text;
        document.getElementById("summary").innerHTML=body.summary;
        document.getElementsByClassName("heading")[0].style.visibility="visible";
        document.getElementsByClassName("container")[0].style.visibility="visible";
        document.getElementsByClassName("heading")[0].style.display="flex";
        document.getElementsByClassName("container")[0].style.display="flex";
      });
    });
  }
  createPPT(ev) {
    ev.preventDefault();

    // const data = new FormData();
    // data.append('text', this.state.text1);
    // data.append('summary', this.state.summary1);
    // data.append('mapping', this.state.mapping);

    fetch('http://localhost:5000/ppt', {
      method: 'POST',
      body: JSON.stringify(this.state),
      headers: new Headers({
        "content-type": "application/json"
      }),
    }).then((response) => {
      response.json().then((body) => {
        this.setState({ ppt_path: body.ppt_path });
        console.log(this.state.ppt_path);
        document.getElementById("download_link").innerHTML="Click here to Download";
      });
    });
    
  }
  //then(res => res.text()).then(text => console.log(text));
  render() {
    return (
      
    <div>
    {/* style={{backgroundColor:"#8CC152"}}> */}
      <form onSubmit={this.handleUploadImage}>
        <div>
          <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
        </div>
        <div>
          <input ref={(ref) => { this.fileName = ref; }} type="text" placeholder="Enter the desired name of file" />
        </div>
        <br />
        <div>
          <button>Upload</button>
        </div>

        <div className="heading">
          <div className="left-col">
            <h1>Text</h1>
          </div>
          
          <div className="center-col">
            <h1>Summary</h1>
          </div>
        </div>
        
        <div className="container">
          <div className="left-col" id="text">
            Left col
          </div>
          
          <div className="center-col" id="summary">
            <span>List</span>
            <ul>
              Hello World
            </ul>
          </div>
        </div>

      </form>
      <br></br>
      <button onClick={this.createPPT}>Create PPT</button>
      <a href={"http://localhost:5000/return-files?pptpath="+ this.state.ppt_path} id="download_link" download> </a>
    </div>
    );
  }
}

export default Main;