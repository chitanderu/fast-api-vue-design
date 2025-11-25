<template>
  <div class="app-container">
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" plain icon="Plus" @click="handleAdd">新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="success" plain icon="Edit" :disabled="single" @click="handleUpdate">编辑</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="danger" plain icon="Delete" :disabled="multiple" @click="handleDelete">删除</el-button>
      </el-col>
      <right-toolbar @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="noteList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="序号" width="80" align="center" prop="noteId" />
      <el-table-column label="内容" min-width="200" prop="content" :show-overflow-tooltip="true" />
      <el-table-column label="创建时间" align="center" width="180" prop="createTime">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createTime, '{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total > 0"
      :total="total"
      v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize"
      @pagination="getList"
    />

    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="noteRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="内容" prop="content">
          <el-input
            type="textarea"
            v-model="form.content"
            :rows="6"
            placeholder="请输入笔记内容"
            maxlength="2000"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { getCurrentInstance, onMounted, reactive, ref, toRefs } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { addNote, deleteNote, listNotes, updateNote } from '@/api/system/note'
import { parseTime } from '@/utils/ruoyi'

const { proxy } = getCurrentInstance()

const noteList = ref([])
const loading = ref(true)
const open = ref(false)
const total = ref(0)
const title = ref('')
const ids = ref([])
const single = ref(true)
const multiple = ref(true)

const data = reactive({
  form: {
    noteId: undefined,
    content: ''
  },
  queryParams: {
    pageNum: 1,
    pageSize: 10
  },
  rules: {
    content: [
      { required: true, message: '笔记内容不能为空', trigger: 'blur' },
      { min: 1, max: 2000, message: '长度应在 1 到 2000 个字符', trigger: 'blur' }
    ]
  }
})

const { form, queryParams, rules } = toRefs(data)

function getList() {
  loading.value = true
  listNotes(queryParams.value).then(response => {
    noteList.value = response.rows
    total.value = response.total
    loading.value = false
  })
}

function reset() {
  form.value = {
    noteId: undefined,
    content: ''
  }
  proxy.resetForm('noteRef')
}

function handleAdd() {
  reset()
  open.value = true
  title.value = '新增笔记'
}

function handleUpdate(row) {
  const current = row || noteList.value.find(item => item.noteId === ids.value[0])
  if (!current) return
  reset()
  form.value = { ...current }
  open.value = true
  title.value = '编辑笔记'
}

function handleDelete(row) {
  const noteIds = row?.noteId || ids.value.join(',')
  if (!noteIds) return
  ElMessageBox.confirm('是否确认删除选中的笔记?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => deleteNote(noteIds)).then(() => {
    getList()
    ElMessage.success('删除成功')
  }).catch(() => {})
}

function submitForm() {
  proxy.$refs['noteRef'].validate(valid => {
    if (!valid) return
    const action = form.value.noteId ? updateNote(form.value) : addNote(form.value)
    action.then(() => {
      ElMessage.success(form.value.noteId ? '修改成功' : '新增成功')
      open.value = false
      getList()
    })
  })
}

function cancel() {
  open.value = false
  reset()
}

function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.noteId)
  single.value = selection.length !== 1
  multiple.value = !selection.length
}

onMounted(() => {
  getList()
})
</script>
