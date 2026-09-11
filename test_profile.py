import time
from ai.meeting_analyzer import MeetingAnalyzer

print("Testing QA")
analyzer = MeetingAnalyzer()
res = analyzer.ask("Hi, my name is John and I am working on the project.", "What is my name?")
print(res)
