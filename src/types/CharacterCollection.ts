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
                    {title: 'Eyebrows', type: 'anatomy.eyebrows'},
                    {title: 'Ears', type: 'anatomy.ears'},
                    {title: 'Inner Ears', type: 'anatomy.ears_inner'},
                    {title: 'Furry Ears', type: 'anatomy.furry_ears'},
                    {title: 'Nose', type: 'anatomy.nose'},
                    {title: 'Expression', type: 'anatomy.expression'},
                    {title: 'Tears', type: 'anatomy.expression_crying'},
                    {title: 'Hair', type: 'anatomy.hair'},
                    {title: 'Hair Ext (L)', type: 'anatomy.hairextl'},
                    {title: 'Hair Ext (R)', type: 'anatomy.hairextr'},
                    {title: 'Ponytail', type: 'anatomy.ponytail'},
                    {title: 'Updo', type: 'anatomy.updo'},
                    {title: 'Beard', type: 'anatomy.beard'},
                    {title: 'Mustache', type: 'anatomy.mustache'},
                    {title: 'Wrinkles', type: 'anatomy.wrinkles'},
                    {title: 'Horns', type: 'anatomy.horns'},
                    {title: 'Fins', type: 'anatomy.fins'},
                    {title: 'Tail', type: 'anatomy.tail'},
                    {title: 'Wings', type: 'anatomy.wings'},
                    {title: 'Wing Dots', type: 'anatomy.wings_dots'},
                    {title: 'Wing Edge', type: 'anatomy.wings_edge'},
                    {title: 'Shadow', type: 'anatomy.shadow'},
                    {title: 'Prosthetic Hand', type: 'anatomy.prosthesis_hand'},
                    {title: 'Prosthetic Leg', type: 'anatomy.prosthesis_leg'},
                    {title: 'Wheelchair', type: 'anatomy.wheelchair'},
                ]
            },
            clothes: {
                title: 'Clothes',
                active: ref('torso'),
                tabs: {
                    torso: {
                        title: 'Torso',
                        children: [
                            {title: 'Shirt/Jacket', type: 'clothes.clothes'},
                            {title: 'Vest', type: 'clothes.vest'},
                            {title: 'Jacket', type: 'clothes.jacket', companions: ['clothes.jacket_collar', 'clothes.jacket_trim']},
                            {title: 'Armour', type: 'clothes.armour'},
                            {title: 'Sleeves', type: 'clothes.sleeves'},
                            {title: 'Chainmail', type: 'clothes.chainmail'},
                            {title: 'Shoulders', type: 'clothes.shoulders'},
                            {title: 'Bauldron', type: 'clothes.bauldron'},
                            {title: 'Cape', type: 'clothes.cape'},
                            {title: 'Belt', type: 'clothes.belt'},
                            {title: 'Sash', type: 'clothes.sash'},
                            {title: 'Dress', type: 'clothes.dress'},
                            {title: 'Overalls', type: 'clothes.overalls'},
                            {title: 'Cargo', type: 'clothes.cargo'},
                            {title: 'Bandages', type: 'clothes.bandages'},
                            {title: 'Backpack Straps', type: 'clothes.backpack_straps'},
                        ]
                    },
                    legs: {
                        title: 'Legs',
                        children: [
                            {title: 'Legs', type: 'clothes.legs'},
                            {title: 'Apron', type: 'clothes.apron'},
                            {title: 'Shoes', type: 'clothes.shoes'},
                            {title: 'Shoe Toe', type: 'clothes.shoes_toe'},
                            {title: 'Socks', type: 'clothes.socks'},
                        ]
                    },
                    arms: {
                        title: 'Arms',
                        children: [
                            {title: 'Arms', type: 'clothes.arms'},
                            {title: 'Gloves', type: 'clothes.gloves'},
                            {title: 'Bracers', type: 'clothes.bracers'},
                            {title: 'Wrists', type: 'clothes.wrists'},
                            {title: 'Ring', type: 'clothes.ring'},
                        ]
                    },
                    head: {
                        title: 'Head',
                        children: [
                            {title: 'Hat', type: 'clothes.hat'},
                            {title: 'Visor', type: 'clothes.visor'},
                            {title: 'Headcover', type: 'clothes.headcover'},
                            {title: 'Bandana', type: 'clothes.bandana'},
                            {title: 'Accessory', type: 'clothes.accessory'},
                            {title: 'Earrings', type: 'clothes.earrings'},
                            {title: 'Neck', type: 'clothes.neck'},
                            {title: 'Necklace', type: 'clothes.necklace'},
                            {title: 'Charm', type: 'clothes.charm'},
                        ]
                    }
                }
            },
            injuries: {
                title: 'Injuries',
                children: [
                    {title: 'Arm Wound', type: 'injuries.wound_arm'},
                    {title: 'Rib Wound', type: 'injuries.wound_ribs'},
                    {title: 'Mouth Wound', type: 'injuries.wound_mouth'},
                    {title: 'Eye Wound (L)', type: 'injuries.wound_eye_left'},
                    {title: 'Eye Wound (R)', type: 'injuries.wound_eye_right'},
                    {title: 'Brain Wound', type: 'injuries.wound_brain'},
                ]
            },
            equipment: {
                title: 'Equipment',
                active: ref('weapons'),
                tabs: {
                    weapons: {
                        title: 'Weapons',
                        children: [
                            {title: 'Swords', type: 'equipment.weapon_sword'},
                            {title: 'Blunt', type: 'equipment.weapon_blunt'},
                            {title: 'Polearms', type: 'equipment.weapon_polearm'},
                            {title: 'Ranged', type: 'equipment.weapon_ranged'},
                            {title: 'Magic', type: 'equipment.weapon_magic'},
                            {title: 'Tools', type: 'equipment.weapon'},
                            {title: 'Ammo', type: 'equipment.ammo'},
                            {title: 'Quiver', type: 'equipment.quiver'},
                        ]
                    },
                    shields: {
                        title: 'Shields',
                        children: [
                            {title: 'Shield', type: 'equipment.shield'},
                            {title: 'Shield Trim', type: 'equipment.shield_trim'},
                            {title: 'Shield Paint', type: 'equipment.shield_paint'},
                            {title: 'Shield Pattern', type: 'equipment.shield_pattern'},
                        ]
                    },
                    gear: {
                        title: 'Gear',
                        children: [
                            {title: 'Backpack', type: 'equipment.backpack'},
                        ]
                    }
                }
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