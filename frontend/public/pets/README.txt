图片目录规范（已接入前端）：

/pets/{petId}/stage{stageIndex}.png

例如：
/pets/1/stage1.png
/pets/1/stage2.png
...
/pets/10/stage4.png

要求：
1) 所有图片统一尺寸（推荐 1024x1024）
2) 透明背景 PNG
3) petId 对应后端宠物模板 id（1~10）
4) stageIndex 为 1~4

推荐生成方式（网页端 GPT）：
1) 从 backend/app/seeds/pet_templates.py 复制 image_prompt
2) 在网页端 GPT 生成透明背景 PNG，尺寸 1024x1024
3) 按上面的命名规则保存到本目录
