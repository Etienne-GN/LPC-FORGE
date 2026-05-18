import {ItemCollection} from "@/types/ItemCollection";
import {ref} from "vue";

export class CharacterCollection extends ItemCollection {
    spriteTypes = ['anatomy', 'clothes', 'equipment', 'injuries']

    getSpriteCategories():any {
        return {
            anatomy: {
                title: 'Anatomy',
                children: [
                    {title: 'Body', type: 'anatomy.body'},
                    {title: 'Head', type: 'anatomy.head'},
                    {title: 'Eyes', type: 'anatomy.eyes'},
                    {title: 'Ears', type: 'anatomy.ears'},
                    {title: 'Nose', type: 'anatomy.nose'},
                    {title: 'Hair', type: 'anatomy.hair'},
                    {title: 'Beard', type: 'anatomy.beards'},
                    {title: 'Wrinkles', type: 'anatomy.wrinkles'},
                    {title: 'Tail', type: 'anatomy.tails'},
                    {title: 'Wings', type: 'anatomy.wings'},
                    {title: 'Shadow', type: 'anatomy.shadow'},
                ]
            },
            clothes: {
                title: 'Clothes',
                active: ref('torso'),
                tabs: {
                    torso: {
                        title: 'Torso',
                        children: [
                            {title: 'Torso', type: 'clothes.torso'},
                            {title: 'Shoulders', type: 'clothes.shoulders'},
                            {title: 'Cape', type: 'clothes.cape'},
                            {title: 'Dress', type: 'clothes.dress'},
                        ]
                    },
                    legs: {
                        title: 'Legs',
                        children: [
                            {title: 'Legs', type: 'clothes.legs'},
                            {title: 'Feet', type: 'clothes.feet'},
                        ]
                    },
                    arms: {
                        title: 'Arms',
                        children: [
                            {title: 'Arms', type: 'clothes.arms'},
                        ]
                    },
                    head: {
                        title: 'Head',
                        children: [
                            {title: 'Headwear', type: 'clothes.headwear'},
                        ]
                    }
                }
            },
            injuries: {
                title: 'Injuries',
                children: [
                    {title: 'Wounds', type: 'injuries.wounds'},
                ]
            },
            equipment: {
                title: 'Equipment',
                children: [
                    {title: 'Weapons', type: 'equipment.weapons'},
                    {title: 'Tools', type: 'equipment.tools'},
                    {title: 'Backpack', type: 'equipment.backpack'},
                    {title: 'Quiver', type: 'equipment.quiver'},
                ]
            }
        }
    }

    isBodySelected() {
        return !!this.selected.anatomy?.body
    }

    getTileSize(animation: string): number {
        for (const type in this.selected) {
            for (const category in this.selected[type]) {
                if (!this.selected[type][category]) {
                    continue
                }

                if (!this.selected[type][category].sizes) {
                    continue
                }

                if (!this.selected[type][category].sizes[animation]) {
                    continue
                }

                switch (this.selected[type][category].sizes[animation]) {
                    case 'lg':
                        return 128
                    case 'xl':
                        return 192
                }
            }
        }

        return 64
    }

    isAnimationDisabled(animation: string): boolean {
        return this.isAnimationDisabledForCharacter(animation) && this.isAnimationDisabledForEquipment(animation)
    }

    private isAnimationDisabledForCharacter(animation: string) {
        for (const type of ['anatomy', 'clothes']) {
            for (const category in this.selected[type]) {
                if (!this.selected[type][category]) {
                    continue
                }

                if (this.selected[type][category].animations.indexOf(animation) === -1) {
                    return true
                }
            }
        }

        return false
    }

    private isAnimationDisabledForEquipment(animation: string) {
        const type = 'equipment'

        for (const category in this.selected[type]) {
            if (!this.selected[type][category]) {
                continue
            }

            if (this.selected[type][category].animations.indexOf(animation) >= 0) {
                return false
            }
        }

        return true
    }
}