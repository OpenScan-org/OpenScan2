# How to create a perfect 3d scan

## TLDR
A perfect object's surface for photogrammetry looks something like this:
![perfect surface](https://user-images.githubusercontent.com/57842400/165493134-2781e6df-6e9e-44ec-8a93-12215ea65d59.jpg)
* **thousands of distinct/random features**
* no specular highlights
* no blurry areas
* high contrast

# Guide

It is all about the object's surface and some basic camera and lighting settings. But fortunately, there are some neat little tricks to scan almost any kind of object. The following flow chart gives an overview and should be printed and placed next to your scanner.

**Every new object poses a challenge, so take your time answering each individual question and adjust your workflow accordingly**




Below you can find many examples and explanations.

![DecisionTree](https://user-images.githubusercontent.com/57842400/165475087-9fd507b6-ea02-454a-af5a-b6895f08c3b5.png)

# Table of Contents
1. [OBJECT](#OBJECT)
   * [Plastic Miniature](#plastic-miniature)
   * [Plastic replacment part](#plastic-replacement-part)
   * [Plastic 3D printed miniature](#plastic-3d-printed-miniature)
   * [Metal Key](#metal-key)
   * [Cast Metal Tank Chain](#cast-metal-tank-chain)
   * [Stone spinning whorl (archeology)](#stone-spinning-whorl)
   * [Flintstone tool/weapon](#Stone-flintstone-tool)
   * 
2. [LIGHT](#LIGHT)
   * [Cross polarization](#Cross_polarization)
3. [CAMERA](#CAMERA)

# OBJECT
I am using either the OpenScan Classic or Mini with their ring-light turned on to create the following examples:

## Plastic miniature
| ![figurine1](https://user-images.githubusercontent.com/57842400/165480743-6c4cbcc1-ea7c-4b77-905d-926e91fcbd3e.jpg) | ![figurine2](https://user-images.githubusercontent.com/57842400/165480757-85ac6978-9170-4d95-94f7-fcb3bb87de01.jpg) | ![figurine3](https://user-images.githubusercontent.com/57842400/165480771-ef97c268-86bf-4f8f-8041-32474a56b134.jpg) |  
|:---:|:---:|:---:|
| **bad** | **bad** | **very good** |
| without polarizer | with polarizer | with polarizer and scanning spray |
| The object has large unicolor areas and a lot of specular highlights | The specular highlights can be removed with cross-polarisation (which is not absolutely necessary, but helps in the next step) | Add thousands of tiny dots by applying a fine layer of scanning/chalk spray, the dots could be finer and denser. |

## Plastic replacement part

| ![plastik1](https://user-images.githubusercontent.com/57842400/165482945-b30ccc84-da44-480f-99b0-790bc73c6cf6.jpg)  | ![plastik2b](https://user-images.githubusercontent.com/57842400/165482937-258b015e-0560-402e-a56b-056b1c69967a.jpg) | ![plastik3](https://user-images.githubusercontent.com/57842400/165482758-476a4f0e-bbcb-4c9b-baf6-09472da1c9ff.jpg)  |
|:---:|:---:|:---:|
| **bad** | **okay-ish** |  **perfect** |
| without polarizer | with polarizer | with polarizer and scanning spray |
| The object seems to have a lot of surface features, where in fact it is almost totally unicolor. What you see here are thousands of specular highlights| The specular highlights can be removed with cross-polarisation. Now, you are able to see, that the object is almost completely featureless (except for some small pieces of dirt, which might already be enough.) | Add thousands of tiny dots by applying a fine layer of scanning/chalk spray. This is an example of a perfectly random, feature-rich surface |

## Plastic 3D Printed miniature

|  ![mini1](https://user-images.githubusercontent.com/57842400/165484334-788ccff7-1574-4151-b4e0-50c8e52f1ef0.jpg) |  ![mini2a](https://user-images.githubusercontent.com/57842400/165484371-6e3cf1ac-f4e1-418e-92e0-d7c11e77cc65.jpg) | ![mini3](https://user-images.githubusercontent.com/57842400/165484385-9d512ef0-cd6b-433d-9ca4-ec369f20b227.jpg)  |
|:---:|:---:|:---:|
| **bad** | **bad** |  **perfect** |
| without polarizer | with polarizer | with polarizer and scanning spray |
| Again, the surface seems feature-rich, but all you see are specular highlights created by the surface of the 3d print  | As soon as you add cross-polarization, all those highlights disappear and not many features are left  | Create a perfect, feature-rich surface with the help of some scanning spray  |

## metal key

|  ![key01](https://user-images.githubusercontent.com/57842400/165489805-dc9f1c48-a59b-46e4-aff6-882e21ba09f6.jpg) |  ![key02](https://user-images.githubusercontent.com/57842400/165489817-ba120dc7-2c30-4be7-b1e2-51285494b92e.jpg) | ![key03](https://user-images.githubusercontent.com/57842400/165489838-c192a5be-c3f5-4322-a049-6d444b5425f3.jpg)  |
|:---:|:---:|:---:|
| **bad** | **bad** |  **good** |
| without polarizer | with polarizer | with polarizer and scanning spray |
|  lots of specular highlights and almost no distinct surface features | due to the high reflectivity of the surface, there are still specular highlights visible when using cross-polarisation (this could be avoided in a completely dark environment + polarized light source)  | adding dots helps a lot to create enough features, but the remaining specular highlights might create some noise in the resulting 3d mesh. To improve the result, you would have to matte the surface before applying the scanning spray |

## Cast metal tank chain

| ![cast01](https://user-images.githubusercontent.com/57842400/165490031-8954c361-4fdf-46e2-ae74-2a76ff65c689.jpg)  |  ![cast02](https://user-images.githubusercontent.com/57842400/165490049-3cf85624-2950-4dc5-bb18-436df9f29026.jpg) |
|:---:|:---:|
| **bad** | **very good** | 
| without polarizer | with polarizer  |
|   |   |

## Stone spinning whorl

This is basically as good as it could be, lots of features and almost no specular highlights.  Note, that not all types of stone show that amount of surface features/graininess.

|  ![stone00](https://user-images.githubusercontent.com/57842400/165494355-39d6e219-66eb-4ef0-a83c-5d0a2ea2bba7.jpg) |  ![stone01](https://user-images.githubusercontent.com/57842400/165494185-001b4db0-8284-47a6-adc7-8ec28b5cf01d.jpg) |
|:---:|:---:|
| **perfect** | **perfect** |
|  without polarizer |  with polarizer  |


## Stone flintstone tool

| ![flint01](https://user-images.githubusercontent.com/57842400/165495617-6b594b56-f02d-40dd-a001-33a723731101.jpg) | ![flint02](https://user-images.githubusercontent.com/57842400/165495630-c3af513f-cdfe-46ae-b4c6-1eebd9d517cc.jpg) |
|:---:|:---:|
| **bad** | **good** |
|  without polarizer |  with polarizer  |
| A lot of specular highlights  | The feature on this surface are not very distinct and a little bit washed-out. Scanning spray could definitely help a lot |

## Wood

This is basically as good as it could be, lots of features and almost no specular highlights. Note, that not all types of wood show that amount of surface features/graininess.

| ![wood01](https://user-images.githubusercontent.com/57842400/165497374-e7e22a48-9610-4154-acdf-310a026b13e4.jpg) | ![wood02](https://user-images.githubusercontent.com/57842400/165497402-95676c45-26bb-4854-b731-ec51fa3876e4.jpg) |
|:---:|:---:|
| **perfect** | **perfect** |
|  without polarizer |  with polarizer  |

## Fabric

## Skin

# LIGHT

### Cross_polarization


# CAMERA
