# Video Annotation QA Checklist

Use this checklist for a second-pass review before submission.

## Instruction alignment
- Does the annotation evaluate the exact written instruction?
- Is the final state consistent with the requested outcome?
- Are unrelated actions excluded unless the rubric requires them?

## Temporal boundaries
- Does the action start at the first observable frame of the defined action?
- Does it end at the first frame where the defined end state is achieved?
- Are adjacent actions separated consistently?
- Is there timestamp drift?

## Action and object accuracy
- Is the action verb observable rather than inferred?
- Are the correct actor and object identified?
- Is contact/release/placement described only when visibly supported?
- Are object-state changes captured?

## Description quality
- Is the description concise and neutral?
- Does it avoid guessing intent?
- Does it avoid adding information not visible in the clip?
- Is terminology consistent with the project taxonomy?

## Consistency
- Would the same rule produce the same label on a similar clip?
- Are identical events labeled in the same way?
- Are edge cases handled according to the guideline rather than personal preference?

## Final review
- Rewatch the boundary frames.
- Recheck all low-confidence annotations.
- Resolve or flag ambiguity.
- Confirm required fields are complete.
- Submit only after a second pass.
