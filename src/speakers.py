from pydantic import BaseModel, Field
from typing import List, Dict

class SpeakerConfig(BaseModel):
    name: str = Field(..., description="Name of the speaker")
    description: str = Field(..., description="Description of the speaker characteristcs")
    
Jon = SpeakerConfig(
    name="Jon", 
    description="Jon's voice is monotone yet slightly fast in delivery, with a very close recording that almost has no background noise."
)

Lea = SpeakerConfig(
    name="Lea", 
    description="Lea speaks slightly animatedly and slightly slowly in delivery, with a very close recording that has no background noise."
)

Gary = SpeakerConfig(
    name="Gary", 
    description="Gary speaks slightly animatedly and slightly slowly in delivery, with a very close recording that has no background noise."
)

Jenna = SpeakerConfig(
    name="Jenna", 
    description="Jenna's voice is monotone yet slightly fast in delivery, with a very close recording that almost has no background noise."
)

