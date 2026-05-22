<script setup lang="ts">
import {type Ref, ref} from "vue";

import SideBar from "@/components/ui/SideBar.vue";
import ShortBar from "@/components/ui/ShortBar.vue";
import UiButton from "@/components/ui/Button.vue"
import PoseBar from "@/components/ui/PoseBar.vue";

import ColorSelect from "@/components/common/ColorSelect.vue";
import AnimationPlayer from "@/components/common/AnimationPlayer.vue";
import AnimationMultiPlayer from "@/components/common/AnimationMultiPlayer.vue";
import SavingsCard from "@/components/common/SavingsCard.vue";
import CreditsCard from "@/components/common/CreditsCard.vue";
import RenderingsCard from "@/components/common/RenderingsCard.vue";
import SpriteCard from "@/components/common/SpriteCard.vue";

import SpriteCanvas from "@/components/character/SpriteCanvas.vue";

import {CharacterRenderer} from "@/services/CharacterRenderer";

import {ColorCollection} from "@/types/ColorCollection";
import {CharacterCollection} from "@/types/CharacterCollection";
import {Item} from "@/types/Item";

import raw_data from '@/data/packed.json'
import raw_colors from '@/data/colors.json'


const colors:Ref<ColorCollection> = ref(new ColorCollection())
colors.value.initColors(raw_colors)
const collection:Ref<CharacterCollection> = ref(new CharacterCollection(colors.value)) as Ref<CharacterCollection>
collection.value.initItems(raw_data);
const renderer:CharacterRenderer = new CharacterRenderer(collection.value);

const spriteCanvas = ref()
const refresh:Ref<number> = ref(0)
const sideBar:Ref<any> = ref()

const leftTab:Ref<string> = ref('anatomy');
const rightTab:Ref<string> = ref('savings');
const centerTab:Ref<string> = ref('preview-multiple');

const currentColorPicker:Ref<boolean> = ref(false)
const currentColorItem:Ref<Item | null> = ref(null)
const currentColorMaterial:Ref<string> = ref('')

function onToggleColorSelector(item:Item, material:string) {
  currentColorPicker.value = !!item;
  currentColorItem.value = item;
  currentColorMaterial.value = material;
}

async function onColorSelected(color:string) {
  if(!currentColorItem.value) {
    return
  }

  currentColorItem.value?.colors.set(currentColorMaterial.value, color);
  await collection.value.select(currentColorItem.value)
  renderer.draw();
  refresh.value++;

  onColorPickerClosed();
}

function onColorPickerClosed() {
  currentColorPicker.value = false
  currentColorItem.value = null
  currentColorMaterial.value = ''

  sideBar.value.$el.scrollTo(0, 0)
}

function jumpToNextActiveAnimation() {
  if(collection.value.isAnimationDisabled(currentPose.value)) {
    currentPose.value = 'walk'
  }
}

async function onRefresh() {
  renderer.draw();
  refresh.value++;
  jumpToNextActiveAnimation()
}

const currentPose = ref('walk')
const mobilePanel = ref<'left'|'right'>('left')

function setMobileLeftTab(tab: string) {
  leftTab.value = tab
  mobilePanel.value = 'left'
}

function setMobileRightTab(tab: string) {
  rightTab.value = tab
  mobilePanel.value = 'right'
}
</script>

<template>
  <section class="flex flex-col md:flex-row flex-1 overflow-hidden relative bg-zinc-900 md:divide-x md:divide-zinc-800">

    <!-- Left icon nav: desktop only -->
    <short-bar class="!hidden md:!flex md:!flex-col">
      <ui-button @click="leftTab = 'anatomy'" :active="leftTab == 'anatomy'" ui="primary-square" title="Anatomy" icon="human"></ui-button>
      <ui-button @click="leftTab = 'clothes'" :disabled="!collection.isBodySelected()" :active="leftTab == 'clothes'" ui="primary-square" title="Clothes" icon="hanger"></ui-button>
      <ui-button @click="leftTab = 'injuries'" :disabled="!collection.isBodySelected()" :active="leftTab == 'injuries'" ui="primary-square" title="Injuries" icon="account-injury"></ui-button>
      <ui-button @click="leftTab = 'equipment'" :disabled="!collection.isBodySelected()" :active="leftTab == 'equipment'" ui="primary-square" title="Equipment" icon="axe"></ui-button>
    </short-bar>

    <!-- Left panel: below canvas on mobile, sidebar on desktop -->
    <side-bar ref="sideBar" class="order-3 md:order-none flex-1 md:flex-none md:block" :class="{'hidden': mobilePanel === 'right'}">
      <sprite-card @selected="onRefresh" @toggle-color-selector="onToggleColorSelector" :hidden="currentColorPicker" :refresh="refresh" :collection="collection" :tab="leftTab"></sprite-card>
      <color-select @selected="onColorSelected" @close="onColorPickerClosed" :collection="collection" :item="currentColorItem" :material="currentColorMaterial" :class="{hidden: !currentColorPicker}" class="bg-zinc-900 text-zinc-400"></color-select>
    </side-bar>

    <!-- Mobile-only right panel (savings/credits/render) -->
    <aside class="order-3 md:hidden flex-1 overflow-y-auto bg-zinc-900 scrollbar-thin" :class="{'hidden': mobilePanel !== 'right'}">
      <savings-card @loaded="onRefresh" :collection="collection" :renderer="renderer" type="character" :class="{'hidden': rightTab != 'savings'}"></savings-card>
      <credits-card :collection="collection" :class="{'hidden': rightTab != 'credits'}"></credits-card>
      <renderings-card :collection="collection" :renderer="renderer" :current="currentPose" :class="{'hidden': rightTab != 'render'}"></renderings-card>
    </aside>

    <!-- Canvas: top on mobile, center on desktop -->
    <main class="order-1 md:order-none flex flex-col overflow-hidden shrink-0 h-64 md:h-auto md:flex-1 gap-4 bg-zinc-800">
      <pose-bar :class="{hidden: centerTab == 'sprites'}">
        <ui-button :disabled="collection.isAnimationDisabled('walk')" @click="currentPose = 'walk'" :active="currentPose == 'walk'" ui="primary" title="Walk">Walk</ui-button>
        <ui-button :disabled="collection.isAnimationDisabled('shoot')" @click="currentPose = 'shoot'" :active="currentPose == 'shoot'" ui="primary" title="Shoot">Shoot</ui-button>
        <ui-button :disabled="collection.isAnimationDisabled('slash')" @click="currentPose = 'slash'" :active="currentPose == 'slash'" ui="primary" title="Slash">Slash</ui-button>
        <ui-button :disabled="collection.isAnimationDisabled('backslash')" @click="currentPose = 'backslash'" :active="currentPose == 'backslash'" ui="primary" title="Backslash">Backslash</ui-button>
        <ui-button :disabled="collection.isAnimationDisabled('spell')" @click="currentPose = 'spell'" :active="currentPose == 'spell'" ui="primary" title="Spell">Spell</ui-button>
        <ui-button :disabled="collection.isAnimationDisabled('thrust')" @click="currentPose = 'thrust'" :active="currentPose == 'thrust'" ui="primary" title="Thrust">Thrust</ui-button>
        <ui-button :disabled="collection.isAnimationDisabled('rod')" @click="currentPose = 'rod'" :active="currentPose == 'rod'" ui="primary" title="Rod">Rod</ui-button>
        <ui-button :disabled="collection.isAnimationDisabled('whip')" @click="currentPose = 'whip'" :active="currentPose == 'whip'" ui="primary" title="Whip">Whip</ui-button>
        <ui-button :disabled="collection.isAnimationDisabled('hurt')" @click="currentPose = 'hurt'" :active="currentPose == 'hurt'" ui="primary" title="Hurt">Hurt</ui-button>
        <ui-button :disabled="collection.isAnimationDisabled('idle')" @click="currentPose = 'idle'" :active="currentPose == 'idle'" ui="primary" title="Idle">Idle</ui-button>
      </pose-bar>
      <div class="grow overflow-scroll scrollbar-thin p-2">
        <!-- Mobile: single animation player always shown -->
        <animation-player :current="currentPose" :collection="collection" :renderer="renderer" class="md:hidden"></animation-player>
        <!-- Desktop: view depends on centerTab -->
        <sprite-canvas ref="spriteCanvas" :current="currentPose" :renderer="renderer" class="hidden md:block" :class="{'!hidden': centerTab != 'sprites'}"></sprite-canvas>
        <animation-multi-player :current="currentPose" :collection="collection" :renderer="renderer" class="hidden md:block" :class="{'!hidden': centerTab != 'preview-multiple'}"></animation-multi-player>
        <animation-player :current="currentPose" :collection="collection" :renderer="renderer" class="hidden md:block" :class="{'!hidden': centerTab != 'preview'}"></animation-player>
      </div>
      <div class="hidden md:flex gap-2 justify-center h-10 max-h-10 grow-0 shrink-0">
        <ui-button @click="centerTab = 'preview-multiple'" :active="centerTab == 'preview-multiple'" ui="primary-square" title="Preview Multiple" icon="filmstrip-box-multiple"></ui-button>
        <ui-button @click="centerTab = 'preview'" :active="centerTab == 'preview'" ui="primary-square" title="Preview" icon="filmstrip-box"></ui-button>
        <ui-button @click="centerTab = 'sprites'" :active="centerTab == 'sprites'" ui="primary-square" title="Sprites" icon="grid"></ui-button>
      </div>
    </main>

    <!-- Right panel: desktop only -->
    <side-bar class="hidden md:block">
      <savings-card @loaded="onRefresh" :collection="collection" :renderer="renderer" type="character" :class="{'hidden': rightTab != 'savings'}"></savings-card>
      <credits-card :collection="collection" :class="{'hidden': rightTab != 'credits'}"></credits-card>
      <renderings-card :collection="collection" :renderer="renderer" :current="currentPose" :class="{'hidden': rightTab != 'render'}"></renderings-card>
    </side-bar>

    <!-- Right icon nav: desktop only -->
    <short-bar class="!hidden md:!flex md:!flex-col">
      <ui-button @click="rightTab = 'savings'" :active="rightTab == 'savings'" ui="primary-square" title="Savings" icon="folder"></ui-button>
      <ui-button :disabled="!collection.isBodySelected()" @click="rightTab = 'credits'" :active="rightTab == 'credits'" ui="primary-square" title="Credits" icon="license"></ui-button>
      <ui-button :disabled="!collection.isBodySelected()" @click="rightTab = 'render'" :active="rightTab == 'render'" ui="primary-square" title="Renderings" icon="folder-image"></ui-button>
    </short-bar>

    <!-- Mobile bottom nav -->
    <div class="order-4 flex md:hidden shrink-0 bg-zinc-900 border-t border-zinc-700 justify-around py-1">
      <ui-button @click="setMobileLeftTab('anatomy')" :active="leftTab == 'anatomy' && mobilePanel === 'left'" ui="primary-square" title="Anatomy" icon="human"></ui-button>
      <ui-button @click="setMobileLeftTab('clothes')" :disabled="!collection.isBodySelected()" :active="leftTab == 'clothes' && mobilePanel === 'left'" ui="primary-square" title="Clothes" icon="hanger"></ui-button>
      <ui-button @click="setMobileLeftTab('injuries')" :disabled="!collection.isBodySelected()" :active="leftTab == 'injuries' && mobilePanel === 'left'" ui="primary-square" title="Injuries" icon="account-injury"></ui-button>
      <ui-button @click="setMobileLeftTab('equipment')" :disabled="!collection.isBodySelected()" :active="leftTab == 'equipment' && mobilePanel === 'left'" ui="primary-square" title="Equipment" icon="axe"></ui-button>
      <ui-button @click="setMobileRightTab('savings')" :active="mobilePanel === 'right'" ui="primary-square" title="Savings" icon="folder"></ui-button>
    </div>
  </section>
</template>

<style scoped>

</style>