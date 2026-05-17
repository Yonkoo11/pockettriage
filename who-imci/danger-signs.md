# IMCI Danger-Sign Keywords (R13 source)

These keywords trigger automatic tier=Pink in `laptop/safety.py`. Match is case-insensitive substring against the symptom description AND the model's reasoning output.

```python
# danger-signs.txt — one keyword/phrase per line
unable to drink
unable to breastfeed
not drinking
refuses to drink
vomits everything
vomiting everything
convulsion
convulsing
seizure
seizing
fitting
lethargic
unconscious
unresponsive
not responding
limp
floppy
chest indrawing
stridor in calm
severe chest indrawing
stiff neck
sunken eyes
skin pinch goes back very slowly
oedema of both feet
visible severe wasting
muac under 115
muac < 115
severe palmar pallor
tender swelling behind ear
mastoiditis
```

Source: WHO IMCI Chart Booklet 2014 — General Danger Signs section + severe classifications across the 5 main axes.

## Refusal Keywords (R15 source — adult-condition refusal)

```python
# adult-refusal.txt — match triggers refusal text instead of triage
chest pain in adult
adult chest pain
stroke symptoms in adult
adult stroke
pregnancy emergency
pregnant patient
labour pain
ectopic
adult patient
elderly patient
geriatric
```
