
# Probabilistic Safety Map
## Vision-based and Machine Learning techniques.
<p align="center">



<div align="center">
<br />
  <h1 align="center"></h1>

  
  <a href="https://github.com/despargy/RiskTerrainModeling">
    <img src="figs/under-construction.png" alt="Under" width="358" height="235">
  </a>
  <h2 align="center">Probabilistic Safety Map for Secure Footholds</h2> 

</div>

[Upcoming - Update of new function design]
[Upcoming - Upload Unreal Engine-generated dataset]


This work aims to enhance real-time performance in generating a risk map from an image. The objective is to achieve real-time processing, as the analytical computation of the function is time-consuming. Essentially, the goal is to extract a map representation and transform it into a risk map that indicates the probability of each foothold being safe to step on.

Initially, we design a function using analytical computer vision techniques to convert a depth image obtained from an RGB-D image into a risk map based on specific constraints. Subsequently, we generate various random scenes using Unreal Engine to create a dataset that includes objects of interest.

Furthermore, we design a training model to learn the mapping between the depth image and the risk map. Additionally, we explore the possibility of training another model to learn the mapping between an RGB image and the risk map.

Winter semester 2022-2023, Computer Science Department, University of Crete.


Generation of dataset was based on modification of th follwing package:

"SuperCaustics"
https://github.com/MMehdiMousavi/SuperCaustics
</p>
