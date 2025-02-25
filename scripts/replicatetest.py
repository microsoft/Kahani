from diffusionmodels import t2i_models
from visual_processor import VisualProcessor
import os
from PIL import Image


# # "Eye-level, ((28-year-old male, tall, muscular, wheatish skin, deep-set dark brown eyes, black short hair, wearing white khadi kurta-pajama with blue mojari and blue gamcha, curious and hopeful, flipping through a dusty diary, leaning over focused)), ((26-year-old female, slim, fair skin, dark brown wavy braided hair, wearing bright yellow silk saree with floral patterns and red dupatta, gentle smile, encouraging and thoughtful, pointing out important notes, sitting upright)), Ramesh's house porch, evening, clear skies, wicker chairs, kerosene lamp, Indian Rupees symbol in the diary, small INR currency notes peeking from the diary, rural India, Ramesh and Meena examining a dusty diary on their porch, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon",
# character_1 = "Pixar style, eye-level angle, warm evening light, revelatory mood, rustic porch with wicker chairs and kerosene lamp, Ramesh (28, male, Gujarati Patel, farmer, tall, muscular, white khadi kurta-pajama, blue gamcha, curious and hopeful, cross-legged, flipping through a diary), masterpiece, sharp focus, highly detailed, cartoon."
# character_2 = "Pixar style, eye-level angle, warm evening light, revelatory mood, rustic porch with wicker chairs and kerosene lamp, Meena (26, female, Gujarati Patel, homemaker, slim, bright yellow silk saree, red dupatta, encouraging and thoughtful, upright, pointing at notes), masterpiece, sharp focus, highly detailed, cartoon."
# # scene_setting = "Indian Comic Style Illustration, eye-level angle, warm evening light, revelatory mood, rustic porch with wicker chairs and kerosene lamp, Ramesh (28, male, Gujarati Patel, farmer, tall, muscular, white khadi kurta-pajama, blue gamcha, curious and hopeful, cross-legged, flipping through a diary), Meena (26, female, Gujarati Patel, homemaker, slim, bright yellow silk saree, red dupatta, encouraging and thoughtful, upright, pointing at notes), cultural artifacts include wicker chairs and kerosene lamp, financial symbols like INR notes in the diary, Ramesh and Meena discover cryptic financial strategies in a dusty diary, masterpiece, sharp focus, highly detailed, cartoon."
t2i_class = t2i_models()
visualprocessor = VisualProcessor()

# character_1 = "Pixar style, wide shot camera angle, warm evening lighting, harmonious and fortitude mood, living room with a family ledger and traditional kitchen wares, rural Indian home setting, Ramesh (28, male, Gujarati farmer, tall, muscular, white khadi kurta-pajama, blue gamcha, confident and empowered, leading the discussion), masterpiece, sharp focus, highly detailed, cartoon."
# character_2 = "Pixar style, wide shot camera angle, warm evening lighting, harmonious and fortitude mood, living room with a family ledger and traditional kitchen wares, rural Indian home setting, Meena (26, female, Gujarati homemaker, slim, bright yellow silk saree, red dupatta, determined and optimistic, writing notes), masterpiece, sharp focus, highly detailed, cartoon."
# character_3 = "Pixar style, wide shot camera angle, warm evening lighting, harmonious and fortitude mood, living room with a family ledger and traditional kitchen wares, rural Indian home setting, Radha (19, female, Gujarati student, petite, green salwar-kameez, silver bangles, hopeful and enthusiastic, asking questions),  masterpiece, sharp focus, highly detailed, cartoon."
# scene_setting = "Pixar style, wide shot camera angle, warm evening lighting, harmonious and fortitude mood, living room with a family ledger and traditional kitchen wares, rural Indian home setting, Ramesh (28, male, Gujarati farmer, tall, muscular, white khadi kurta-pajama, blue gamcha, confident and empowered, leading the discussion), Meena (26, female, Gujarati homemaker, slim, bright yellow silk saree, red dupatta, determined and optimistic, writing notes), Radha (19, female, Gujarati student, petite, green salwar-kameez, silver bangles, hopeful and enthusiastic, asking questions), cultural artifacts include family ledger with INR symbols, masterpiece, sharp focus, highly detailed, cartoon."

character_1 = "Pixar Style, Eye-level to capture both characters closely, Warm evening glow, Revelatory, A rustic porch in a rural home in Dewas, Madhya Pradesh. The setting sun casts a golden hue over the scene, highlighting the wicker chairs and a kerosene lamp on the ground. The atmosphere is calm and filled with promise., <Character Details> (Ramesh Patel, 28, Male, Gujarati Patel, Farmer, Tall and muscular with deep-set eyes and thick black hair, Wearing a white khadi kurta-pajama with block print, blue mojari, and a blue gamcha. Focused and curious, leaning over a dusty diary, flipping through its pages.), (Kids illustration), masterpiece, sharp focus, white background, highly detailed, cartoon." 
# character_1_pose = "Pixar style, wide shot camera angle, (Ramesh Patel, 28, Male, Gujarati Patel, Farmer, Tall and muscular with deep-set eyes and an aquiline nose, Wearing a white khadi kurta-pajama with blue mojari and a blue gamcha. His posture is inclined forward, desperate for advice., Sitting on a wooden stool, nodding as he listens intently., Desperate for guidance.), (Kids illustration), masterpiece, sharp focus, white background, highly detailed, cartoon."
character_2 = "Pixar Style, Eye-level to capture both characters closely, Warm evening glow, Revelatory, A rustic porch in a rural home in Dewas, Madhya Pradesh. The setting sun casts a golden hue over the scene, highlighting the wicker chairs and a kerosene lamp on the ground. The atmosphere is calm and filled with promise., <Character Details> (Meena Patel, 26, Female, Gujarati Patel, Homemaker, Slim with a heart-shaped face and wavy braided hair, Wearing a bright yellow silk saree with floral patterns, a red dupatta, and a gold mangalsutra. Encouraging and thoughtful, sitting upright and pointing out important notes in the diary.), (Kids illustration), masterpiece, sharp focus, white background, highly detailed, cartoon."
scene_setting = "Pixar Style, Eye-level to capture both characters closely, Warm evening glow, Revelatory, A rustic porch in a rural home in Dewas, Madhya Pradesh. The setting sun casts a golden hue over the scene, highlighting the wicker chairs and a kerosene lamp on the ground. The atmosphere is calm and filled with promise., <Character Details> ((Ramesh Patel, 28, Male, Gujarati Patel, Farmer, Tall and muscular with deep-set eyes and thick black hair, Wearing a white khadi kurta-pajama with block print, blue mojari, and a blue gamcha. Focused and curious, leaning over a dusty diary, flipping through its pages.), (Meena Patel, 26, Female, Gujarati Patel, Homemaker, Slim with a heart-shaped face and wavy braided hair, Wearing a bright yellow silk saree with floral patterns, a red dupatta, and a gold mangalsutra. Encouraging and thoughtful, sitting upright and pointing out important notes in the diary.)), <Cultural Artifacts> Wicker chairs and a kerosene lamp, symbolizing rural simplicity and traditional living. The diary contains small INR currency notes and the Indian Rupee symbol, representing financial discovery., <Specific Actions> Ramesh flips through the pages of the diary with intense focus, while Meena thoughtfully points out important notes. Both are seated cross-legged on the porch, immersed in their discovery., <Scene Description> On the quaint porch of their rustic home, Ramesh and Meena uncover a diary filled with cryptic financial strategies, illuminated by the soft glow of the setting sun. The scene captures their curiosity and hope for a better future., <Artistic Enhancements> (Kids illustration), masterpiece, sharp focus, highly detailed, cartoon>"
# character_1_prompt = visualprocessor.encode_image_to_data_uri("/home/t-dsudharsan/KaryaKahaniPipeline/outputs-new/ramesh/character_assets/Ramesh_Patel_refined.png")
character_1_image = t2i_class.flux_replicate(character_1,"","test1.png")
# character_2_prompt = visualprocessor.encode_image_to_data_uri("/home/t-dsudharsan/KaryaKahaniPipeline/outputs-new/ramesh/character_assets/Meena_Patel_refined.png")
character_2_image = t2i_class.flux_replicate(character_2,"","test2.png")

combined_characters_prompt = visualprocessor.combine_images(["test1.png", "test2.png"], "combined_test.png")
combined_image_prompt = visualprocessor.encode_image_to_data_uri("combined_test.png")
combined_image = t2i_class.flux_replicate(scene_setting,combined_image_prompt,"combined_test_scene.png")
# character_1_pose_image = t2i_class.flux_replicate(character_1_pose,character_prompt,"test1_pose.png")



# character_1_master = "/home/t-dsudharsan/KaryaKahaniPipeline/outputs-new/ramesh/character_assets/pixar/Ramesh_Patel.png"
# imageprompt1 = visualprocessor.encode_image_to_data_uri(character_1_master)
# character_1_image = t2i_class.flux_replicate(character_1,imageprompt1,"test1.png")
# character_2_master = "/home/t-dsudharsan/KaryaKahaniPipeline/outputs-new/ramesh/character_assets/pixar/Meena_Patel.png"
# imageprompt2 = visualprocessor.encode_image_to_data_uri(character_2_master)
# character_2_image = t2i_class.flux_replicate(character_2,imageprompt2,"test2.png")

# character_3_master = "/home/t-dsudharsan/KaryaKahaniPipeline/outputs-new/ramesh/character_assets/pixar/Radha_Patel.png"
# imageprompt3 = visualprocessor.encode_image_to_data_uri(character_3_master)
# character_3_image = t2i_class.flux_replicate(character_3,imageprompt3,"test3.png")

# combined_characters_prompt = visualprocessor.combine_images(["test1.png", "test2.png","test3.png"], "combined_test.png")
# combined_image_prompt = visualprocessor.encode_image_to_data_uri("combined_test.png")
# combined_image = t2i_class.flux_replicate(scene_setting,combined_image_prompt,"combined_test_scene.png")




































# # # ORIGINAL
# # # "Eye-level perspective, ((Young man, 28, traditional cream-colored kurta and white dhoti, medium skin tone, angular face, short neatly combed black wavy hair, anxious, rubbing his forehead while staring at the ledger with furrowed brows)), ((Middle-aged woman, 55, simple cotton sari with minimalistic silver jewelry, medium skin tone, oval face with light wrinkles and kind eyes, gray hair tied neatly in a low bun, concerned, leaning slightly forward with hands clasped, looking at the young man with a piercing, maternal gaze)), Family Jewelry Shop in Ahmedabad, warm and sunny late afternoon, display cases of jewelry, traditional Gujarati decorations, traditional jewelry, Gujarati craft motifs, ledger with red marks, piles of receipts, rural India, The jewelry shop is bustling with activity, yet the middle-aged woman quietly observes the young man's financial missteps. A ledger sits open, red marks indicating debts. Display cases shimmer with jewelry that the young man crafted, telling a story of skill but also financial recklessness. The middle-aged woman's concerned gaze is maternal and wise as she prepares to address her son., (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"

# # character_1 = "Young man, 28, traditional cream-colored kurta and white dhoti, medium skin tone, angular face, short neatly combed black wavy hair, anxious, rubbing his forehead while staring at the ledger with furrowed brows, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"

# # character_2 = "Middle-aged woman, 55, simple cotton sari with minimalistic silver jewelry, medium skin tone, oval face with light wrinkles and kind eyes, gray hair tied neatly in a low bun, concerned, leaning slightly forward with hands clasped, maternal gaze, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"

# # # scene_setting = "Eye-level perspective, Family Jewelry Shop in Ahmedabad, warm and sunny late afternoon, display cases of jewelry, traditional Gujarati decorations, traditional jewelry, Gujarati craft motifs, ledger with red marks, piles of receipts, rural India, The jewelry shop is bustling with activity, yet the middle-aged woman quietly observes the young man's financial missteps. A ledger sits open, red marks indicating debts. Display cases shimmer with jewelry that the young man crafted, telling a story of skill but also financial recklessness. The middle-aged woman's concerned gaze is maternal and wise as she prepares to address her son., (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"

# # scene_setting = "Eye-level perspective, ((Young man, 28, traditional cream-colored kurta and white dhoti, medium skin tone, angular face, short neatly combed black wavy hair, anxious, rubbing his forehead while staring at the ledger with furrowed brows)), ((Middle-aged woman, 55, simple cotton sari with minimalistic silver jewelry, medium skin tone, oval face with light wrinkles and kind eyes, gray hair tied neatly in a low bun, concerned, leaning slightly forward with hands clasped, looking at the young man with a piercing, maternal gaze)), Family Jewelry Shop in Ahmedabad, warm and sunny late afternoon, display cases of jewelry, traditional Gujarati decorations, traditional jewelry, Gujarati craft motifs, ledger with red marks, piles of receipts, rural India, The jewelry shop is bustling with activity, yet the middle-aged woman quietly observes the young man's financial missteps. A ledger sits open, red marks indicating debts. Display cases shimmer with jewelry that the young man crafted, telling a story of skill but also financial recklessness. The middle-aged woman's concerned gaze is maternal and wise as she prepares to address her son., (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"


# # # character_1_image = t2i_class.flux_t2i(character_1)
# # # character_1_image.save("tempassets/character_1_image.png")
# character_1_image = t2i_class.flux_replicate(character_1,"","tempassets/character_1_image2.png")

# # # # character_2_image = t2i_class.flux_t2i(character_2)
# # # # character_2_image.save("tempassets/character_2_image.png")
# character_2_image = t2i_class.flux_replicate(character_2,"","tempassets/character_2_image2.png")

# # character_3_image = t2i_class.flux_replicate(character_3,"","tempassets/character_3_image2.png")

# combined_characters_prompt = visualprocessor.combine_images(["tempassets/character_1_image2.png", "tempassets/character_2_image2.png","tempassets/character_3_image2.png"], "tempassets/combined_characters2.png")
# # combined_characters_prompt = visualprocessor.combine_images(["tempassets/modifiedoutput.png", "tempassets/modifiedoutput2.png","tempassets/modifiedoutput3.png"], "tempassets/combined_modified_output.png")

# # scenes_folder_path = "tempassets"
# # module_id = 1
# # scene_id = 1
# # image_name = f"module_{module_id}_scene_{scene_id}.png"
# # # Initialize the image path (note the filetype should be png)
# # image_path = os.path.join(scenes_folder_path, image_name)

# combined_characters_prompt = visualprocessor.encode_image_to_data_uri("/home/t-dsudharsan/KaryaKahaniPipeline/outputs-new/ramesh/character_assets/pixar/Ramesh_Patel.png")
# scene_image = t2i_class.flux_replicate(character_1,combined_characters_prompt,"test.png")

# image_prompt = Image.open("/home/t-dsudharsan/KaryaKahaniPipeline/scripts/tempassets/character_1_image.png")
# scene_image = t2i_class.flux_img2img(scene_setting,combined_image)
# # scene_image.save(image_path)

# image_prompt = visualprocessor.encode_image_to_data_uri("/home/t-dsudharsan/KaryaKahaniPipeline/scripts/tempassets/character_1_image.png")
# prompt = "Pixar style, eye-level angle, warm evening light, revelatory mood, rustic porch with wicker chairs and kerosene lamp, Ramesh (28, male, Gujarati Patel, farmer, tall, muscular, white khadi kurta-pajama, blue gamcha, curious and hopeful, cross-legged, flipping through a diary), masterpiece, sharp focus, highly detailed, cartoon."
# # output = t2i_class.flux_pulid(prompt,image_prompt,"test.png")
# # output = t2i_class.flux_fofd(prompt,image_prompt,"test.png")
# scene_image = t2i_class.flux_img2img(prompt,image_prompt)
# scene_image.save("test.png")

