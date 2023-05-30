name: 🚀 Feature Request
description: Suggest a RearFold AI idea
# title: " "
labels: [enhancement]
body:
  - type: markdown
    attributes:
      value: |
        Thank you for submitting a RearFold AI 🚀 Feature Request!

  - type: checkboxes
    attributes:
      label: Search before asking
      description: >
        Please search the [issues](https://github.com/RearFold/RearFold-AI/issues) to see if a similar feature request already exists.
      options:
        - label: >
            I have searched the RearFold AI [issues](https://github.com/RearFold/RearFold-AI/issues) and found no similar feature requests.
          required: true

  - type: textarea
    attributes:
      label: Description
      description: A short description of your feature.
      placeholder: |
        What new feature would you like to see in RearFold AI?
    validations:
      required: true

  - type: textarea
    attributes:
      label: Use case
      description: |
        Describe the use case of your feature request. It will help us understand and prioritize the feature request.
      placeholder: |
        How would this feature be used, and who would use it?

  - type: textarea
    attributes:
      label: Additional
      description: Anything else you would like to share?
