<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<div>
<h3 align="center">trace_metals</h3>

  <p align="center">
    A project to determine how and why the circulation of the North Pacific was so particularly strange during the Late Pliocene and Early Pleistocene.
    <br />
    <a href="https://github.com/FmDG/trace_metals"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/FmDG/trace_metals">View Demo</a>
    ·
    <a href="https://github.com/FmDG/trace_metals/issues">Report Bug</a>
    ·
    <a href="https://github.com/FmDG/trace_metals/issues">Request Feature</a>
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
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->

## About The Project

This project looks at producing images and graphics for my PhD project looking at the Pacific Ocean circulation during
the Late Pliocene and Early Pleistocene and determining what role trace metals can play in uncovering past changes.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

<img src="https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/python.svg" alt="drawing" width="15"/> Python


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->

## Getting Started

To set up this project you need to clone the full project into a local directory and then it 
should be possible to run all the relevant functions. If you want to produce some plots which
have been used before then you want to go to Methods/paper/main.py which will allow you to 
produce the figures which are used in de Graaf et al., _in print_.

### Prerequisites
The standard functions are required which are installed as below.
* matplotlib
    ```sh
    pip install matplotlib
    ```
* pandas
* scipy
* numpy

There are also a couple of more distinct prerequisites required for functionality such as
the palaeo-salinity calculations.

* gsw
    ```sh
    pip install gsw
    ```

### Installation

1. Clone the repo.
   ```sh
   git clone https://github.com/FmDG/trace_metals.git
   ```
2. Install the relevant directories.
3. Run the main.py function in methods/paper/main.py.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->

## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos
work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->

## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/FmDG/trace_metals/issues) for a full list of proposed features (and known
issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any
contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also
simply open an issue with the tag "enhancement".

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

Friso de Graaf - f.m.degraaf@qmul.ac.uk

Project Link: [https://github.com/FmDG/trace_metals](https://github.com/FmDG/trace_metals)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

* Heather Ford
* David Thornalley
* [Natalie Burls](https://natalieburls.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/FmDG/trace_metals.svg?style=for-the-badge

[contributors-url]: https://github.com/FmDG/trace_metals/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/FmDG/trace_metals.svg?style=for-the-badge

[forks-url]: https://github.com/FmDG/trace_metals/network/members

[stars-shield]: https://img.shields.io/github/stars/FmDG/trace_metals.svg?style=for-the-badge

[stars-url]: https://github.com/FmDG/trace_metals/stargazers

[issues-shield]: https://img.shields.io/github/issues/FmDG/trace_metals.svg?style=for-the-badge

[issues-url]: https://github.com/FmDG/trace_metals/issues

[license-shield]: https://img.shields.io/github/license/FmDG/trace_metals.svg?style=for-the-badge

[license-url]: https://github.com/FmDG/trace_metals/master/LICENSE.txt

[Python.com]: https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/python.svg


