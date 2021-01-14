import React, { Component } from 'react';
import Gallery from 'react-grid-gallery';
import CheckButton from './CheckButton';
import { Upload, Button, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import axios from "axios";
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      images: [],
      selectAllChecked: false,
      fileList: [],
      uploading: false
    };

    this.onSelectImage = this.onSelectImage.bind(this);
    this.getSelectedImages = this.getSelectedImages.bind(this);
    this.onClickSelectAll = this.onClickSelectAll.bind(this);
    this.handleDeleteImages = this.handleDeleteImages.bind(this);
  }

  componentDidMount() {
    // display all imgs in the db
    axios.get("http://localhost:5000/api/display")
      .then(res => {
        console.log(res)
        // parse the img array
        let images = this.convertData(res, "display_list")

        this.setState({
          images: images
        })
      }).catch(e => {
        console.log(e)
      });
  }

  convertData(res, list_key) {
    let displayList = res["data"][list_key]
    let images = displayList.map(img_info => {
      let img_link = `${img_info["url"]}${img_info["key"]}${img_info["file_ext"]}`

      return {
        "src": img_link,
        "thumbnail": img_link,
        "thumbnailWidth": 250,
        "thumbnailHeight": 250,
        "caption": img_info["file_name"],
        "imgKey": img_info["key"]
      }
    })

    return images
  }

  allImagesSelected(images) {
    var f = images.filter(
      function (img) {
        return img.isSelected == true;
      }
    );
    return f.length == images.length;
  }

  onSelectImage(index, image) {
    var images = this.state.images.slice();
    var img = images[index];
    if (img.hasOwnProperty("isSelected"))
      img.isSelected = !img.isSelected;
    else
      img.isSelected = true;

    this.setState({
      images: images
    });

    if (this.allImagesSelected(images)) {
      this.setState({
        selectAllChecked: true
      });
    }
    else {
      this.setState({
        selectAllChecked: false
      });
    }
  }

  getSelectedImages() {
    var selected = [];
    for (var i = 0; i < this.state.images.length; i++)
      if (this.state.images[i].isSelected == true)
        selected.push(this.state.images[i].imgKey);
    return selected;
  }

  onClickSelectAll() {
    var selectAllChecked = !this.state.selectAllChecked;
    this.setState({
      selectAllChecked: selectAllChecked
    });

    var images = this.state.images.slice();
    if (selectAllChecked) {
      for (var i = 0; i < this.state.images.length; i++)
        images[i].isSelected = true;
    }
    else {
      for (var i = 0; i < this.state.images.length; i++)
        images[i].isSelected = false;

    }
    this.setState({
      images: images
    });
  }

  handleUpload = () => {
    const { fileList } = this.state;
    let formData = new FormData();
    fileList.forEach(file => {
      formData.append('imgFiles[]', file);
    });

    // Display the key/value pairs
    for (var pair of formData.entries()) {
      console.log(pair[0] + ', ' + pair[1]);
    }

    this.setState({
      uploading: true,
    });

    axios.post("http://localhost:5000/api/upload", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
      .then(res => {
        console.log(res)
        let new_items = this.convertData(res, "added_items");
        this.setState({
          fileList: [],
          uploading: false,
          images: this.state.images.concat(new_items)
        });
      }).catch(e => {
        this.setState({
          uploading: false,
        });
        console.log(e);
      });
  }

  handleDeleteImages() {
    let imgsToDelete = this.getSelectedImages()
    console.log(imgsToDelete)

    axios.delete("http://localhost:5000/api/delete", {
      data: {
        img_id_list: imgsToDelete
      }
    })
      .then(res => {
        console.log(res)
        let deletedKeys = res["data"]["deleted_keys"];
        let resSet = new Set(deletedKeys);
        let images = this.state.images;
        let newImages = images.filter((imgData) => {
          if (!resSet.has(imgData.imgKey)) {
            return imgData
          }
        })

        this.setState({
          images: newImages
        })
      }).catch(e => {
        console.log(e)
      });
  }

  render() {
    const { uploading, fileList } = this.state;
    const props = {
      onRemove: file => {
        this.setState(state => {
          const index = state.fileList.indexOf(file);
          const newFileList = state.fileList.slice();
          newFileList.splice(index, 1);
          return {
            fileList: newFileList,
          };
        });
      },
      beforeUpload: file => {
        this.setState(state => ({
          fileList: [...state.fileList, file],
        }));
        return false;
      },
      multiple: true,
      fileList,
    };

    return (
      <div>
        <h1> Shopify Summer 2021 Image Repository Challenge </h1>
        <CheckButton
          index={0}
          isSelected={this.state.selectAllChecked}
          onClick={this.onClickSelectAll}
          parentHover={true}
          color={"rgba(0,0,0,0.54)"}
          selectedColor={"#4285f4"}
          hoverColor={"rgba(0,0,0,0.54)"} />
        <div style={{
          height: "36px",
          display: "flex",
          alignItems: "center"
        }}>
          select all
      </div>
        <Upload {...props}>
          <Button icon={<UploadOutlined />}>Select File</Button>
        </Upload>
        <Button
          type="primary"
          onClick={this.handleUpload}
          disabled={fileList.length === 0}
          loading={uploading}
          style={{ marginTop: 16 }}
        >
          {uploading ? 'Uploading' : 'Start Upload'}
        </Button>

        {this.getSelectedImages().length ? <Button onClick={this.handleDeleteImages} variant="danger">Delete Selected</Button> : null}
        <div style={{
          display: "block",
          minHeight: "1px",
          width: "100%",
          border: "1px solid #ddd",
          overflow: "auto"
        }}>
          Click the Checkmark in the Top Left corner of image to select them.
          <Gallery
            images={this.state.images}
            onSelectImage={this.onSelectImage}
            showLightboxThumbnails={true} />
        </div>
      </div>
    )
  }
}


export default App;
