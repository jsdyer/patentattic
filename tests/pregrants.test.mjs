import test from 'node:test';
import assert from 'node:assert/strict';
import {preGrantCatalog} from '../web/pregrants.mjs';
test('keeps application and grant identifiers distinct and exposes IPC and queue',()=>{
  const edition = {count:1,updated:'2026-11-17',rows:[['3016489','GEARING SYSTEM','MOVE MOBILITY GMBH','B62M 3/06','2022-02-09',1,'Révision technique / Technical Review']]};
  const [row]=preGrantCatalog(edition).records;
  assert.equal(row.b,'Technical Review');
  assert.match(row.a,/transport/);
  assert.equal(row.date,'2022-02-09');
  assert.equal(row.fields['Queue position in this edition'],1);
  assert.ok(row.links[0].url.endsWith('/3016489/summary.html'));
});
