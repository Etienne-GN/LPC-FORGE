<script setup lang="ts">
import {type Ref, ref, watch} from 'vue'

import UiDropdown from "@/components/ui/Dropdown.vue";
import type {ItemCollection} from "@/types/ItemCollection";
import type {Item} from "@/types/Item";
import type {Color} from "@/types/Color";

const props = defineProps<{
  type: string,
  title: string,
  refresh: number,
  collection: ItemCollection
}>()

const emit = defineEmits(['selected'])

const selected: Ref<Item> = ref(props.collection.getSelected(props.type)) as Ref<Item>

// ── color picker state ───────────────────────────────────────────────────────
const pickerMaterial = ref<string>('')

function togglePicker(material: string) {
  pickerMaterial.value = pickerMaterial.value === material ? '' : material
}

function closePicker() {
  pickerMaterial.value = ''
}

function currentMaterialDef() {
  if (!selected.value || !pickerMaterial.value) return null
  return selected.value.materials[pickerMaterial.value] ?? null
}

function isShown(color: Color, palette: string): boolean {
  return color.materials.indexOf(palette) >= 0
}

async function onColorSelected(colorKey: string) {
  if (!selected.value) return
  selected.value.colors.set(pickerMaterial.value, colorKey)
  await props.collection.select(selected.value)
  emit('selected', selected)
  closePicker()
}

// ── variant state ────────────────────────────────────────────────────────────
const VARIANT_CSS: {[key: string]: string} = {
  black: '#1a1a1a', charcoal: '#3c3c3c', shadow: '#4a4a5a', soot: '#2a2a2a',
  gray: '#888', silver: '#bbb', smoke: '#ccc', dove: '#d8d8d8', white: '#f0f0f0',
  ivory: '#fffff0', pearl: '#eee8d5', ice: '#e8f0ff', platinum: '#e5e4e2',
  red: '#cc2222', garnet: '#8b1a1a', wine: '#722f37', maroon: '#800000', ruby: '#9b111e',
  orange: '#e65c00', coral: '#ff6b47', red_orange: '#cc4400', copper: '#b87333',
  yellow: '#ddb800', gold: '#ccaa00', amber: '#ffbf00', lemon: '#fff44f',
  blonde: '#f5deb3', sandy: '#daa520', ginger: '#b5651d',
  green: '#225522', forest: '#228b22', olive: '#6b8e23', fern: '#4f7942',
  mint: '#98ff98', spring: '#00ff7f', emerald: '#50c878', apple: '#8db600',
  blue: '#2244aa', navy: '#001166', sky: '#6699dd', aegean: '#3a7ebf',
  teal: '#008080', cyan: '#00bbcc', cerulean: '#007ba7', denim: '#1560bd',
  azure: '#007fff', royal: '#4169e1', cornflower: '#6495ed', powder: '#b0e0e6',
  purple: '#660066', violet: '#8b00ff', lavender: '#9966cc', amethyst: '#9966cc',
  indigo: '#4b0082', plum: '#8e4585', mauve: '#e0b0ff', heather: '#b086ac',
  pink: '#dd66aa', rose: '#ff007f', cerise: '#de3163',
  brown: '#553311', leather: '#8b5a2b', walnut: '#5c4033', chocolate: '#7b3f00',
  umber: '#635147', sepia: '#704214', tan: '#d2b48c', beige: '#f5f0d7',
  linen: '#faf0e6', peach: '#ffc8a2', apricot: '#fbceb1', salmon: '#fa8072',
  oak: '#806040', ash_brown: '#7d6a57', bluegray: '#6a8ba4', slate: '#708090',
}

function variantCss(v: string): string {
  return VARIANT_CSS[v] ?? '#777'
}

async function onVariantSelect(variant: string) {
  if (!selected.value) return
  selected.value.setVariant(variant)
  await props.collection.select(selected.value)
  emit('selected', selected)
}

// ── shared helpers ───────────────────────────────────────────────────────────
function swatchColor(material: any) {
  const c = selected.value.colors.find(selected.value.colors.getCurrent(material))?.palette[2]
  return c ? `rgb(${c[0]},${c[1]},${c[2]})` : ''
}

function hasNoSwatches() {
  return !selected.value || !selected.value.id ||
    (Object.keys(selected.value.materials).length === 0 && !selected.value.variants?.length)
}

function getOptions() {
  return props.collection.getFilteredOptions(props.type)
}

async function onSelect(itemId: string) {
  closePicker()
  if (itemId) {
    selected.value = await props.collection.select(itemId)
  } else {
    props.collection.unselect(props.type)
    selected.value = props.collection.getSelected(props.type) as Item
  }
  emit('selected', selected)
}

watch(() => props.refresh, () => {
  selected.value = props.collection.getSelected(props.type) as Item
})
</script>

<template>
  <div v-if="Object.keys(getOptions()).length > 0">
    <h2 class="text-xs text-zinc-400 font-bold">{{ title }}</h2>

    <div class="flex my-1">
      <ui-dropdown @selected="onSelect" :selected="collection.getSelected(type)" :options="getOptions()" :type="type"
                   :class="{'rounded-r': hasNoSwatches()}"></ui-dropdown>

      <template v-if="selected">
        <!-- runtime-recolorable: one swatch per material -->
        <button v-for="(matDef, matKey, index) in selected.materials"
                :key="matKey"
                @click="togglePicker(matKey as string)"
                :title="matDef.name"
                class="min-w-8 w-8 p-1 bg-zinc-700"
                :class="{
                  'rounded-r': index === Object.keys(selected.materials).length - 1 && !selected.variants?.length,
                  'bg-zinc-500': pickerMaterial === matKey
                }">
          <div class="h-full rounded" :style="{ backgroundColor: swatchColor(matKey) }"></div>
        </button>

        <!-- pre-colored variants: one tiny swatch per variant -->
        <template v-if="selected.variants && selected.variants.length > 1">
          <button v-for="(v, i) in selected.variants" :key="v"
                  @click="onVariantSelect(v)" :title="v"
                  class="min-w-5 w-5 p-0.5 bg-zinc-700"
                  :class="{ 'rounded-r': i === selected.variants.length - 1,
                             'outline outline-1 outline-amber-400': selected.variant === v }">
            <div class="h-full w-full rounded" :style="{ backgroundColor: variantCss(v) }"></div>
          </button>
        </template>
      </template>
    </div>

    <!-- inline color picker menu, opens below the row -->
    <div v-if="pickerMaterial && currentMaterialDef()"
         class="mb-2 rounded border border-zinc-600 bg-zinc-800 text-zinc-200 text-xs overflow-hidden">
      <div class="flex items-center px-2 py-1 bg-zinc-700 border-b border-zinc-600">
        <span class="font-bold flex-grow">{{ currentMaterialDef()?.name }}</span>
        <button @click="closePicker" class="text-zinc-400 hover:text-zinc-100 ml-2">
          <i class="mdi mdi-close"></i>
        </button>
      </div>
      <div class="max-h-52 overflow-y-auto scrollbar-thin">
        <template v-for="palette in currentMaterialDef()?.palettes" :key="palette">
          <template v-for="(colorVal, colorKey) in collection.colors.getAll()" :key="colorKey">
            <div v-if="isShown(colorVal, palette)"
                 class="flex items-center px-2 py-1 cursor-pointer hover:bg-zinc-600"
                 :class="{ 'bg-zinc-600': selected?.colors?.getCurrent(pickerMaterial) === colorKey }"
                 @click="onColorSelected(colorKey as string)">
              <span class="flex-grow">{{ colorVal.name }}</span>
              <div class="grid grid-cols-6 w-24 h-4 flex-shrink-0">
                <div v-for="(shade, si) in colorVal.palette" :key="si"
                     :class="{ 'rounded-l': si===0, 'rounded-r': si===colorVal.palette.length-1 }"
                     :style="{ backgroundColor: `rgb(${shade[0]},${shade[1]},${shade[2]})` }"></div>
              </div>
            </div>
          </template>
        </template>
      </div>
    </div>

  </div>
</template>
