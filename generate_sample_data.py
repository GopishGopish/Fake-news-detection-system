import pandas as pd
import os

# Create a more substantial dummy dataset for better training metrics
data = {
    'title': [
        "Scientific Breakthrough: New Energy Source Found",
        "Economic Growth Sets New Record This Quarter",
        "Local Hero Saves Family from House Fire",
        "Mars Rover Discovers Ancient Water Channels",
        "Global Climate Summit Reaches Historic Agreement",
        "New Medical Treatment Shows Promise for Rare Diseases",
        "SpaceX Successfully Launches Next-Gen Satellite",
        "Historic Library Restored to Former Glory",
        "Local Team Wins National Championship",
        "Advancements in AI Lead to Better Medical Diagnoses",
        "Renewable Energy Jobs on the Rise Globally",
        "New Park Opens in City Center for Families",
        "Tech Giants Commit to Reducing Electronic Waste",
        "Breakthrough in Ocean Cleanup Technology",
        "Local Farmers Market Celebrates 50th Anniversary",
        "Alien Invasion: UFOs Landing in Major Cities",
        "Magic Pill Makes You Lose 50 Pounds in One Day",
        "Secret Government Plot to Replace Humans with Robots",
        "Celebrity Spotted Flying Without a Plane",
        "Ancient Pyramid Discovered on the Moon",
        "Invisibility Cloak Now Available for $10",
        "Eat Chocolate to Live Forever, Study Says",
        "Time Traveler Claims Tomorrow Will Never Come",
        "Talking Dog Elected Mayor of Small Town",
        "Sun to Turn Purple Next Week, Scientists Warn",
        "Drink Salt Water to Cure All Illnesses",
        "Billionaire accidentally sends entire fortune to random cat",
        "Zombies spotted in local shopping mall says witness",
        "Moon landing was filmed in a basement claims actor",
        "Gravity to be turned off for maintenance tomorrow"
    ],
    'text': [
        "Researchers at the National Fusion Laboratory have reported a sustained reaction that produces more energy than it consumes, a holy grail for clean energy.",
        "The national GDP grew by 4.5% this quarter, the highest rate in two decades, driven by strong consumer spending and tech exports.",
        "A local citizen was awarded a medal of bravery after rescuing a family of four from their burning residence in the middle of the night.",
        "High-resolution images from the latest orbiter show unmistakable signs of river deltas and lake beds across the Jovian surface.",
        "Delegates from over 150 nations have finalized a plan to reach net-zero emissions by 2050, including strict enforcement mechanisms.",
        "Clinical trials for a new mRNA-based drug have shown a 90% success rate in treating a previously incurable genetic disorder.",
        "The Falcon 10 rocket successfully deployed 60 communication satellites into low earth orbit this morning before landing its booster.",
        "The city's central library, built in 1890, has completed a $50 million restoration that preserves its historic character while adding digital labs.",
        "In a thrilling sudden-death overtime, the city's home team clinched the national trophy for the first time in history.",
        "A multi-center study has proven that deep learning algorithms can detect early-stage lung cancer with higher precision than human radiologists.",
        "Global reports indicate that employment in the wind and solar sectors has doubled in the last year as nations shift away from coal.",
        "The new 'Green Heart' park opened today, featuring three hectares of playground, walking trails, and sustainable urban drainage systems.",
        "Leaders of the five largest technology firms signed a pact today to ensure 100% of their products are recyclable by the year 2030.",
        "A new autonomous fleet of interceptors has successfully cleared 5,000 tons of plastic from the Great Pacific Garbage Patch in its first month.",
        "The community gathered today to celebrate the local farmers market, which has provided fresh produce and supported local growers since 1974.",
        "Thousands of unidentified flying objects have been spotted over New York and London. Officials say they are definitely from another galaxy and are attacking.",
        "A revolutionary new supplement has been released that allows anyone to lose massive amounts of weight instantly without any diet or exercise.",
        "Leaked documents reveal that the world's most powerful leaders are actually androids controlled by a secret shadow organization from deep space.",
        "A famous actor was seen by hundreds of fans levitating and flying through the air in downtown Los Angeles yesterday with no harness or aircraft.",
        "Astronauts on a secret mission have found a massive stone pyramid on the dark side of the moon, identical to those found in Egypt.",
        "A tech startup claims to have created a cheap invisibility cloak using light-bending plastic, now selling for just ten dollars on the dark web.",
        "Newly discovered ancient scrolls suggest that eating three kilograms of dark chocolate daily can stop the aging process completely.",
        "A man appearing in a silver suit in Times Square claims to be from the year 3000 and warns that time will stop exactly at midnight tonight.",
        "Residents of a rural town have voted a golden retriever as their mayor after a landslide victory, claiming the dog has better policies than humans.",
        "NASA astronomers are baffled as new data suggests the sun's outer layer will change its color to purple due to a cosmic dust cloud passing by.",
        "Follow this simple trick: drinking two liters of ocean water every morning will flush all toxins and cure every known disease instantly.",
        "A technical glitch at a major bank caused a billionaire's entire savings to be transferred to a domestic cat's microchip account.",
        "Shoppers fled in terror today as witnesses claim to have seen multiple undead individuals wandering through the food court of the local mall.",
        "A retired camera technician has produced documents that allegedly prove the entire moon mission was filmed in a soundstage in Nevada.",
        "The Department of Physics has announced that Earth's gravity will be temporarily suspended for two hours tomorrow for vital repairs."
    ],
    'label': ['REAL']*15 + ['FAKE']*15
}

df = pd.DataFrame(data)
current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(current_dir, 'dataset')
if not os.path.exists(dataset_dir):
    os.makedirs(dataset_dir)
save_path = os.path.join(dataset_dir, 'news.csv')
df.to_csv(save_path, index=False)
print(f"Substantial sample dataset (30 rows) created successfully at {save_path}")
