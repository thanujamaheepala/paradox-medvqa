import React, {Fragment, useEffect, useState } from 'react'
import axios from 'axios';

const Uploader = () => {
    const [selectedFile, setSelectedFile] = useState()
    const [preview, setPreview] = useState()
    const [isUploaded, setIsUploaded] = useState(false)

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

            // try {
            //     const response = await axios({
            //       method: "post",
            //       url: "http://localhost:5000/upload",
            //       data: formData,
            //       headers: { "Content-Type": "multipart/form-data" },
            //     });
            //   } catch(error) {
            //     console.log(error)
            // }

            // fetch(
            //     'http://localhost:5000/upload',
            //     {
            //         method: 'POST',
            //         body: formData,
            //     }
            // )
            //     .then((response) => response.json())
            //     .then((result) => {
            //         console.log('Success:', result)
            //         setIsUploaded(true)
            //     })
            //     .catch((error) => {
            //         console.error('Error:', error)
            //         setIsUploaded(false)
            //     })
        }	
	}
    const handleChange = () => {
        setIsUploaded(false)
	}

    return (
        <Fragment>
            <div><label className="form-label" htmlFor="customFile">Image</label>
            <input type="file" accept=".jpg,.jpeg,.png" className="form-control rounded border border-dark" id="file" onChange={onSelectFile}/>
            {!isUploaded &&   <button type="button" className="btn btn-dark btn-block mt-2" onClick={handleUpload}>Upload</button> }
            {isUploaded &&   <button type="button" className="btn btn-dark btn-block mt-2" onClick={handleChange}>Change</button> }
            </div>
            {(selectedFile && isUploaded) &&  <img src={preview} className="img-fluid rounded border border-dark mt-4" alt="Responsive image" /> }
        </Fragment>
    )
}

export default Uploader

