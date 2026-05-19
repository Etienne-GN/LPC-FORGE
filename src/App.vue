<script setup lang="ts">
import '@mdi/font/css/materialdesignicons.css'
import CharacterView from '@/components/CharacterView.vue'
import HorseView from '@/components/HorseView.vue'
import RacePresetsView from '@/components/RacePresetsView.vue'

import {ref, watch, type Ref} from 'vue'

import {ColorCollection} from "@/types/ColorCollection";
import {CharacterCollection} from "@/types/CharacterCollection";
import {CharacterRenderer} from "@/services/CharacterRenderer";

import raw_data from '@/data/packed.json'
import raw_colors from '@/data/colors.json'

const colors:Ref<ColorCollection> = ref(new ColorCollection())
colors.value.initColors(raw_colors)
const collection:Ref<CharacterCollection> = ref(new CharacterCollection(colors.value)) as Ref<CharacterCollection>
collection.value.initItems(raw_data);
const renderer:CharacterRenderer = new CharacterRenderer(collection.value);

let tab = ref('character');

</script>

<template>
  <div class="flex flex-col h-screen bg-zinc-900 scrollbar-thumb-amber-950 scrollbar-track-transparent scrollbar-thumb-rounded">
    <header class="flex bg-zinc-900 text-zinc-300 h-16 px-4 items-center gap-4 border-b border-zinc-800">
      <div class="flex gap-2 w-96 items-center text-zinc-400">
        <img :src="'logo.png'" class="border-zinc-600 border-2 rounded-full h-11 bg-zinc-800">
        <h1>LPC Forge</h1>
      </div>
      <div class="grow flex gap-2 justify-center">
        <button @click="tab = 'character'" class="p-1 px-2 rounded" :class="{'bg-zinc-700': tab == 'character', 'hover:bg-zinc-800': tab != 'character'}"><i class="mdi mdi-human"></i> Character</button>
        <button @click="tab = 'races'" class="p-1 px-2 rounded" :class="{'bg-zinc-700': tab == 'races', 'hover:bg-zinc-800': tab != 'races'}"><i class="mdi mdi-account-group"></i> Races</button>
        <button @click="tab = 'horse'" class="p-1 px-2 rounded" :class="{'bg-zinc-700': tab == 'horse', 'hover:bg-zinc-800': tab != 'horse'}"><i class="mdi mdi-horse"></i> Horse</button>
      </div>
      <div class="text-right w-96">
        <a href="https://www.github.com/vitruvianstudio" target="_blank" class="text-2xl"><i class="mdi mdi-github"></i></a>
      </div>
    </header>
    <div class="h-[0px]"></div>

    <character-view v-if="tab == 'character'" :collection="collection" :renderer="renderer"></character-view>
    <race-presets-view v-if="tab == 'races'" :collection="collection" :renderer="renderer"></race-presets-view>
    <horse-view v-if="tab == 'horse'"></horse-view>

    <footer class="h-10 flex items-center justify-center bg-zinc-800 text-zinc-500 text-sm border-t border-zinc-700">LPC Forge — sprites from Universal LPC Spritesheet Character Generator</footer>
  </div>
</template>

<style scoped>

</style>
