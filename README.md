<!-- Improved compatibility of back to top link: See: https://github.com/ncsyvn/microservices-flask-python-example/pulls -->
<a name="page-top"></a>
<!--
*** Thanks for checking out the "microservices-flask-python-example". If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->


[[Contributor]][contributors-url]
[[Forks]][forks-url]
[[Stargazers]][stars-url]
[[Issues]][issues-url]
[[MIT License]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ncsyvn/microservices-flask-python-example">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Microservices Flask Python Example</h3>

  <p align="center">
    Start with some basic application
    <br />
</p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#test-service">Test Service</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


This source show you a basic microservices system with python language and Flask framework.
There are 2 mini services that connect directly with its apis:
* Authentication service
    * signup
    * login
* Video service
    * create new video
    * get list videos

<a href="https://github.com/ncsyvn/microservices-flask-python-example/images/microservices-architecture.png">
    <img src="images/microservices-architecture.png" alt="Architecture">
</a>
<p align="right">(<a href="#page-top">back to top</a>)</p>



### Built With

This section should list any major frameworks/libraries used for your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [![Python][python-shield]][python-url]
* [![Flask][flask-shield]][flask-url]

<p align="right">(<a href="#page-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* [[Download python 3.7]][download-python-url]
* [[Install pip]][install-pip-url]
* [[Download and install mysql database]][download-mysql-url]
* [[Download postman to testing api]][download-postman-url]

  
### Installation

Below is an instruction for installing and setting up auth_service. Do the same with video_service.

1. Clone the repo
   ```sh
   git clone https://github.com/ncsyvn/microservices-flask-python-example.git
   ```
2. Install library
   ```sh
   * Create virtual environent (venv/conda/...)
   * Active venv in terminal
   * pip install -r auth_service/requirements.txt
   ```
3. Migrate db

    After migrate database successfully, we will have "migrations" folder in auth_app. 
    Besides, in mysql db, we will see 2 new tables: user, token
   ```sh
   * Change database uri in settings file:
     Example: SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/auth_service'
   * Open new terminal -> Go to "auth_service/auth_app" folder
   * cmd: 
         1. flask db init
         2. flask db migrate -m "message you want"
         3. flask db upgrade  
   ```

4. Run code
    
    After install step 2&3 with both auth_service and video_service. 

    Run 2 apps in 2 different ports (example: 5012 & 5013).
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Test service -->
## Test service
This is the postman collection to testing your API
* [[Postman collection]][postman-testing-url]
<div align="center">
    <h12>Create new video with valid token example</h12>
</div>
<a href="https://github.com/ncsyvn/microservices-flask-python-example/images/create-video-success-with-token.png">
    <img src="images/create-video-success-with-token.png" alt="Create video success with valid token">
</a>
<div align="center">
    <h12>Create new video with failed without token</h12>
</div>
<a href="https://github.com/ncsyvn/microservices-flask-python-example/images/create-video-failed-without-token.png">
    <img src="images/create-video-failed-without-token.png" alt="Create video failed without">
</a>
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Cong Sy Nguyen - ncsyvn@gmail.com

Other projects: [https://github.com/ncsyvn?tab=repositories](https://github.com/ncsyvn?tab=repositories)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[python-shield]: https://img.shields.io/static/v1?label=python&message=v3.7&color=green
[flask-shield]: https://img.shields.io/static/v1?label=flask&message=2.0.1&color=green
[contributors-shield]: https://img.shields.io/github/contributors/ncsyvn/microservices-flask-python-example.svg?style=for-the-badge
[contributors-url]: https://github.com/ncsyvn/microservices-flask-python-example/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ncsyvn/microservices-flask-python-example.svg?style=for-the-badge
[forks-url]: https://github.com/ncsyvn/microservices-flask-python-example/network/members
[stars-shield]: https://img.shields.io/github/stars/ncsyvn/microservices-flask-python-example.svg?style=for-the-badge
[stars-url]: https://github.com/ncsyvn/microservices-flask-python-example/stargazers
[issues-shield]: https://img.shields.io/github/issues/ncsyvn/microservices-flask-python-example.svg?style=for-the-badge
[issues-url]: https://github.com/ncsyvn/microservices-flask-python-example/issues
[license-shield]: https://img.shields.io/github/license/ncsyvn/microservices-flask-python-example.svg?style=for-the-badge
[license-url]: https://github.com/ncsyvn/microservices-flask-python-example/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[product-screenshot]: images/screenshot.png
[python-url]: https://www.python.org/
[flask-url]: https://flask.palletsprojects.com
[download-python-url]: https://www.python.org/downloads/
[install-pip-url]: https://pip.pypa.io/en/stable/installation/
[download-mysql-url]: https://dev.mysql.com/downloads/installer/
[download-postman-url]: https://www.postman.com/
[postman-testing-url]: https://elements.getpostman.com/redirect?entityId=8820631-7d76b73e-dc98-41f1-b16e-cfafed1bd431&entityType=collection
