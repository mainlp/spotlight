# Spotlight 
This is the repository for the Spotlight approach presented in the ACL paper "[What's the Difference? Supporting Users in Identifying the Effects of Prompt and Model Changes Through Token Patterns](https://aclanthology.org/2025.acl-long.985/)".

If you are looking for the data mining method used as core component in Spotlight, please go to the [PyPremise](https://github.com/m-hedderich/PyPremise) library.

## Abstract

Prompt engineering for large language models is challenging, as even small prompt perturbations or model changes can significantly impact the generated output texts. Existing evaluation methods of LLM outputs, either automated metrics or human evaluation, have limitations, such as providing limited insights or being labor-intensive. We propose Spotlight, a new approach that combines both automation and human analysis. Based on data mining techniques, we automatically distinguish between random (decoding) variations and systematic differences in language model outputs. This process provides token patterns that describe the systematic differences and guide the user in manually analyzing the effects of their prompts and changes in models efficiently. We create three benchmarks to quantitatively test the reliability of token pattern extraction methods and demonstrate that our approach provides new insights into established prompt data. From a human-centric perspective, through demonstration studies and a user study, we show that our token pattern approach helps users understand the systematic differences of language model outputs. We are further able to discover relevant differences caused by prompt and model changes (e.g. related to gender or culture), thus supporting the prompt engineering process and human-centric model behavior research. 

## Tutorial
We will provide a Jupyter notebook tutorial on how to use the Spotlight framework in combination with the Premise algorithm here [coming very soon].

At the moment, just use the original [PyPremise](https://github.com/m-hedderich/PyPremise) library and interpret "correct/incorrect classification" with "group 1/2".


## Repository Structure

This repository contains two main folders:
- **data**: benchmarks, prompt dataset and demonstration study outputs, all pattern results for all pattern extraction methods, and the results of the user study.
- **code**: to generate the benchmarks, to run the pattern extraction methods, and the full user study server and interface.

Please take a look at the README file in each subfolder for more information. 

## Contact & Citation

If you run into any issues using this repo or the Spotlight approach in general, do not hesitate to contact us (e-mail in the publication) or create an issue on Github.

If you use this approach in your work, we would be happy if you tell us about it.

If you use Spotlight in your academic work, please cite

```
@inproceedings{hedderich-etal-2025-whats,
    title = "What{'}s the Difference? Supporting Users in Identifying the Effects of Prompt and Model Changes Through Token Patterns",
    author = "Hedderich, Michael A.  and
      Wang, Anyi  and
      Zhao, Raoyuan  and
      Eichin, Florian  and
      Fischer, Jonas  and
      Plank, Barbara",
    booktitle = "Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    year = "2025",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.acl-long.985/"
}
```
