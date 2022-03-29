import React, {Fragment, useEffect, useState } from 'react'
import axios from 'axios';
import Header from './components/Header'
import { ThreeDots } from  'react-loader-spinner'

function App() {
  const [selectedFile, setSelectedFile] = useState()
    const [preview, setPreview] = useState()
    const [isUploaded, setIsUploaded] = useState(false)
    const [data, setData] = useState([
   
    ])

    // create a preview as a side effect, whenever selected file is changed
    useEffect(() => {
        if (!selectedFile) {
            setPreview(undefined)
            return
        }

        const objectUrl = URL.createObjectURL(selectedFile)
        setPreview(objectUrl)

        // free memory when ever this component is unmounted
        return () => URL.revokeObjectURL(objectUrl)
    }, [selectedFile])

    const onSelectFile = e => {
        if (!e.target.files || e.target.files.length === 0 || !(e.target.files[0]['type'].split('/')[0] === 'image')) {
            setSelectedFile(undefined)
            return
        }
        setIsUploaded(false)
        setData([])
        // I've kept this example simple by using the first image instead of multiple
        setSelectedFile(e.target.files[0])
    }

    const handleUpload = () => {
        if (selectedFile) {
            const formData = new FormData()

		    formData.append('file', selectedFile)
            formData.append('filename', selectedFile.name)
            let url = "http://localhost:5000/upload";

            axios.post(url, formData, { // receive two parameter endpoint url ,form data 
            })
            .then(res => { // then print response status
                console.warn(res);
                setIsUploaded(true)
            }).catch(error => {
                console.error('There was an error!', error);
                setIsUploaded(false)
            });
        }	
	}
    const handleChange = () => {
        setIsUploaded(false)
  }

  const onSubmit = e => {
      const q = document.getElementById("question").value
      const filteredQ = q.replace(/[^a-zA-Z0-9 ]/g, '');
      const prevData = data
      if(filteredQ.length !== 0){
          const newData = [{ q: filteredQ.concat("?"),a: false}].concat(prevData)
          setData(newData)
          document.getElementById("question").value = ""

          const formData = new FormData()

          formData.append('question',filteredQ)
          formData.append('filename', selectedFile.name)

          let url = "http://localhost:5000/predict";

          axios.post(url, formData, { // receive two parameter endpoint url ,form data 
          })
          .then(res => { // then print response status
              const newData = [{ q: filteredQ.concat("?"),a: res.data}].concat(prevData)
              setData(newData)
              console.log(res)
          }).catch(error => {
              console.error('There was an error!', error);
              var newData = data
              newData.pop(0)
              setData(newData)
          });
      }   
  }

  return (
    <app>
      <div className="row mt-4 text-center">
        <div className="col-md-4 offset-md-4">
          <Header/>
        </div>
      </div>
      <div className="row mt-4 text-center ">
        <div className="col-md-4 offset-md-2">
          <Fragment>
              <div><label className="form-label" htmlFor="customFile">Image</label>
              <input type="file" accept=".jpg,.jpeg,.png" className="form-control rounded border border-dark" id="file" onChange={onSelectFile}/>
              {!isUploaded &&   <button type="button" className="btn btn-dark btn-block mt-2" onClick={handleUpload}>Upload</button> }
              {isUploaded &&   <button type="button" className="btn btn-dark btn-block mt-2" disabled onClick={handleUpload}>Upload</button> }
              </div>
              {(selectedFile && isUploaded) &&  <img src={preview} className="img-fluid rounded border border-dark mt-4" alt="Responsive image" /> }
          </Fragment>
        </div>
        <div className="col-md-4 offset-md-0">
          <Fragment>
              <div>
              <label className="form-label" htmlFor="question">Question</label>
              <input type="text" className="form-control rounded border border-dark" id="question" disabled = {(!isUploaded)? "disabled" : ""} />
              <button type="button" className="btn btn-dark btn-block mt-2" onClick={onSubmit} disabled = {(!isUploaded)? "disabled" : ""}>Submit</button>
              </div>
              {(data.length===0) ? (
                  <div></div>
              ) : (
                  <div className="rounded border border-dark mt-4 overflow-auto" style={{height: "45vh"}} >
              {data.map((datum, index) => (
              <div className="mb-4 mt-2 mr-1"  key={index}>
                  <h6 style={{paddingLeft: "10px", textAlign: "left"}}>Q: {datum.q}</h6>
                  {datum.a===false && <ThreeDots color="#00BFFF" height={20} width={100} />}
                  {!datum.a===false &&   <p style={{paddingLeft: "30px", textAlign: "left"}}>A: {datum.a}</p> }
              </div>
              ))}
              </div>
              )}
              
          </Fragment>
        </div>
      </div>
    </app>   
  )
}


export default App;
