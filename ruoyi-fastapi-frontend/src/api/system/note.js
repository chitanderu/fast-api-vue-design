import request from '@/utils/request'

export function listNotes(query) {
  return request({
    url: '/system/note/list',
    method: 'get',
    params: query
  })
}

export function addNote(data) {
  return request({
    url: '/system/note',
    method: 'post',
    data
  })
}

export function updateNote(data) {
  return request({
    url: '/system/note',
    method: 'put',
    data
  })
}

export function deleteNote(noteIds) {
  return request({
    url: `/system/note/${noteIds}`,
    method: 'delete'
  })
}
